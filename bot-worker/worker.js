/**
 * Telegram-webhook bot dla strony BAD ANGEL (Cloudflare Worker).
 *
 * Telegram -> webhook -> ten worker -> commit do GitHuba (contents API).
 * Push PAT-em wyzwala workflow deploy, który sam buduje stronę (build.py).
 *
 * Sekrety (wrangler secret put): TELEGRAM_TOKEN, GH_TOKEN, WEBHOOK_SECRET.
 * KV binding: STATE (admini, panel: stany oczekiwania na wpis, kategoria zdjęć).
 *
 * UI: panel z przyciskami (inline keyboard) + stare komendy tekstowe.
 */

const REPO = "rostyslavescaperoomsupplier-arch/bad-angel";

const CATEGORY_ALIASES = {
  "маникюр": "manicure", "manicure": "manicure", "ногти": "manicure",
  "педикюр": "pedicure", "pedicure": "pedicure",
  "ресницы": "rzesy", "rzesy": "rzesy", "рэсницы": "rzesy", "вии": "rzesy",
  "брови": "brwi", "brwi": "brwi",
  "массаж": "masaz", "masaz": "masaz", "масаж": "masaz",
  "депиляция": "depilacja", "depilacja": "depilacja", "депіляція": "depilacja",
  "спа": "spa", "spa": "spa",
  "шрамы": "blizny", "blizny": "blizny", "шрами": "blizny",
  "волосы": "wlosy", "wlosy": "wlosy", "косички": "wlosy", "волосся": "wlosy",
};
const CATEGORY_RU = {
  manicure: "Маникюр", pedicure: "Педикюр", rzesy: "Ресницы", brwi: "Брови",
  masaz: "Массаж", depilacja: "Депиляция", spa: "СПА", blizny: "Шрамы", wlosy: "Волосы",
};
const CATEGORY_LIST = "маникюр, педикюр, ресницы, брови, массаж, депиляция, спа, шрамы, волосы";

const HELP =
  "Привет! Я обновляю сайт badangelsalonpiękności.pl\n\n" +
  "Жми кнопки внизу — там всё: прайс, фото, отзывы.\n\n" +
  "Можно и текстом: пришли фото с подписью-категорией " +
  `(<i>${CATEGORY_LIST}</i>), или команды ` +
  "<code>цены маникюр</code>, <code>цена маникюр 3 120</code>, " +
  "<code>услуга маникюр Название | 120</code>, <code>удалить маникюр 3</code>, " +
  "<code>отзывы 1300</code>.\n\n" +
  "После моего ✅ сайт обновляется ещё около 2 минут.";

export default {
  async fetch(request, env) {
    if (request.method !== "POST") return new Response("ok");
    if (request.headers.get("X-Telegram-Bot-Api-Secret-Token") !== env.WEBHOOK_SECRET)
      return new Response("forbidden", { status: 403 });

    let update;
    try { update = await request.json(); } catch { return new Response("ok"); }

    try {
      if (update.callback_query) await handleCallback(update.callback_query, env);
      else if (update.message) await handleMessage(update.message, env);
    } catch (e) {
      const chatId = update.callback_query?.message?.chat?.id || update.message?.chat?.id;
      if (chatId) { try { await send(env, chatId, "⚠️ Ошибка: " + e.message); } catch {} }
    }
    return new Response("ok"); // zawsze 200, żeby Telegram nie powtarzał update'u
  },
};

// ---------- klawiatury ----------

const MAIN_KB = {
  inline_keyboard: [
    [{ text: "💰 Прайс", callback_data: "price:cats" }],
    [{ text: "👩‍🎨 Мастера", callback_data: "masters:list" }],
    [{ text: "📸 Добавить фото", callback_data: "photo:cats" }],
    [{ text: "⭐ Число отзывов", callback_data: "reviews:ask" }],
  ],
};

function translitSlug(name, existing) {
  const map = { а:"a",б:"b",в:"v",г:"g",д:"d",е:"e",ё:"e",ж:"zh",з:"z",и:"i",й:"i",к:"k",л:"l",м:"m",н:"n",о:"o",п:"p",р:"r",с:"s",т:"t",у:"u",ф:"f",х:"h",ц:"c",ч:"ch",ш:"sh",щ:"sch",ъ:"",ы:"y",ь:"",э:"e",ю:"yu",я:"ya",і:"i",ї:"yi",є:"ye",ґ:"g" };
  let s = name.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/ł/g, "l");
  s = [...s].map(c => map[c] !== undefined ? map[c] : c).join("");
  s = s.replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "mistrz";
  let slug = s, n = 2;
  while (existing.includes(slug)) slug = `${s}-${n++}`;
  return slug;
}

function masterListKb(masters) {
  const rows = masters.map(m => [{ text: `${m.name} — ${m.role}`.slice(0, 60), callback_data: `masters:view:${m.slug}` }]);
  rows.push([{ text: "➕ Добавить мастера", callback_data: "masters:add" }]);
  rows.push([{ text: "⬅️ Меню", callback_data: "menu" }]);
  return { inline_keyboard: rows };
}

function masterText(m) {
  const cats = (m.serves || []).map(s => CATEGORY_RU[s] || s).join(", ") || "—";
  return `👩‍🎨 <b>${m.name}</b>\n${m.role}\nУслуги: ${cats}` + (m.bio && m.bio.length ? `\n\n${m.bio.join("\n\n")}` : "");
}

function masterKb(slug) {
  return {
    inline_keyboard: [
      [{ text: "✏️ Услуги", callback_data: `masters:srv:${slug}` },
       { text: "✏️ Роль", callback_data: `masters:role:${slug}` }],
      [{ text: "📷 Фото", callback_data: `masters:photo:${slug}` },
       { text: "✏️ Описание", callback_data: `masters:bio:${slug}` }],
      [{ text: "🗑 Удалить", callback_data: `masters:del:${slug}` }],
      [{ text: "⬅️ Мастера", callback_data: "masters:list" }],
    ],
  };
}

function servesKb(slug, serves) {
  const slugs = Object.keys(CATEGORY_RU);
  const rows = [];
  for (let i = 0; i < slugs.length; i += 3)
    rows.push(slugs.slice(i, i + 3).map(s => ({
      text: (serves.includes(s) ? "✅ " : "▫️ ") + CATEGORY_RU[s],
      callback_data: `masters:srvt:${slug}:${s}`,
    })));
  rows.push([{ text: "💾 Сохранить", callback_data: `masters:srvs:${slug}` },
             { text: "Отмена", callback_data: `masters:view:${slug}` }]);
  return { inline_keyboard: rows };
}

function catGrid(prefix) {
  const slugs = Object.keys(CATEGORY_RU);
  const rows = [];
  for (let i = 0; i < slugs.length; i += 3)
    rows.push(slugs.slice(i, i + 3).map(s => ({ text: CATEGORY_RU[s], callback_data: `${prefix}:${s}` })));
  rows.push([{ text: "⬅️ Меню", callback_data: "menu" }]);
  return { inline_keyboard: rows };
}

function numGrid(prefix, n, backData) {
  const rows = [];
  for (let i = 0; i < n; i += 5)
    rows.push(Array.from({ length: Math.min(5, n - i) }, (_, j) => {
      const k = i + j + 1;
      return { text: String(k), callback_data: `${prefix}:${k}` };
    }));
  rows.push([{ text: "⬅️ Назад", callback_data: backData }]);
  return { inline_keyboard: rows };
}

function priceListText(slug, items) {
  const lines = items.map((it, i) => `${i + 1}. ${it[0]} — <b>${it[3]}</b>${it[2] ? ` (${it[2]})` : ""}`);
  return `💰 <b>${CATEGORY_RU[slug]}</b>:\n` + (lines.join("\n") || "пусто");
}

function priceCatKb(slug) {
  return {
    inline_keyboard: [
      [{ text: "✏️ Изменить цену", callback_data: `price:edit:${slug}` },
       { text: "🗑 Удалить", callback_data: `price:del:${slug}` }],
      [{ text: "➕ Добавить услугу", callback_data: `price:add:${slug}` }],
      [{ text: "⬅️ Категории", callback_data: "price:cats" }],
    ],
  };
}

// ---------- callbacki (przyciski) ----------

async function handleCallback(cb, env) {
  const chatId = cb.message.chat.id;
  const msgId = cb.message.message_id;
  const userId = cb.from.id;
  const admins = JSON.parse((await env.STATE.get("admins")) || "[]");
  if (!admins.includes(userId)) {
    await tg(env, "answerCallbackQuery", { callback_query_id: cb.id, text: "⛔ Нет доступа" });
    return;
  }
  const d = cb.data;
  const ack = (text) => tg(env, "answerCallbackQuery", { callback_query_id: cb.id, ...(text ? { text } : {}) });

  if (d === "menu") {
    await edit(env, chatId, msgId, "Что делаем?", MAIN_KB);
    await ack();

  } else if (d === "price:cats") {
    await env.STATE.delete(`pending:${userId}`);
    await edit(env, chatId, msgId, "💰 Выбери категорию:", catGrid("price:cat"));
    await ack();

  } else if (d.startsWith("price:cat:")) {
    const slug = d.split(":")[2];
    const { data } = await getSiteData(env);
    await edit(env, chatId, msgId, priceListText(slug, data.services[slug] || []), priceCatKb(slug));
    await ack();

  } else if (d.startsWith("price:edit:") && d.split(":").length === 3) {
    const slug = d.split(":")[2];
    const { data } = await getSiteData(env);
    const n = (data.services[slug] || []).length;
    await edit(env, chatId, msgId,
      priceListText(slug, data.services[slug] || []) + "\n\n✏️ Какой услуге меняем цену? Жми номер:",
      numGrid(`price:edit:${slug}`, n, `price:cat:${slug}`));
    await ack();

  } else if (d.startsWith("price:edit:")) {
    const [, , slug, idxs] = d.split(":");
    const idx = Number(idxs);
    const { data } = await getSiteData(env);
    const it = (data.services[slug] || [])[idx - 1];
    if (!it) { await ack("Нет такой услуги"); return; }
    await env.STATE.put(`pending:${userId}`, JSON.stringify({ action: "price", slug, idx }), { expirationTtl: 1800 });
    await send(env, chatId, `✏️ «${it[0]}», сейчас <b>${it[3]}</b>.\nНапиши новую цену (например <code>120</code> или <code>от 120</code>):`);
    await ack();

  } else if (d.startsWith("price:del:") && d.split(":").length === 3) {
    const slug = d.split(":")[2];
    const { data } = await getSiteData(env);
    const n = (data.services[slug] || []).length;
    await edit(env, chatId, msgId,
      priceListText(slug, data.services[slug] || []) + "\n\n🗑 Какую услугу удалить? Жми номер:",
      numGrid(`price:delq:${slug}`, n, `price:cat:${slug}`));
    await ack();

  } else if (d.startsWith("price:delq:")) {
    const [, , slug, idxs] = d.split(":");
    const { data } = await getSiteData(env);
    const it = (data.services[slug] || [])[Number(idxs) - 1];
    if (!it) { await ack("Нет такой услуги"); return; }
    await edit(env, chatId, msgId, `Удалить «${it[0]}» (${it[3]}) из «${CATEGORY_RU[slug]}»?`, {
      inline_keyboard: [[
        { text: "❌ Да, удалить", callback_data: `price:delok:${slug}:${idxs}` },
        { text: "Отмена", callback_data: `price:cat:${slug}` },
      ]],
    });
    await ack();

  } else if (d.startsWith("price:delok:")) {
    const [, , slug, idxs] = d.split(":");
    const { data, sha } = await getSiteData(env);
    const items = data.services[slug] || [];
    const [removed] = items.splice(Number(idxs) - 1, 1);
    if (!removed) { await ack("Нет такой услуги"); return; }
    await putSiteData(env, data, sha, `Bot: usunięta usługa "${removed[0]}" (${slug})`);
    await edit(env, chatId, msgId, `✅ «${removed[0]}» удалена. Сайт обновится через ~2 минуты.\n\n` + priceListText(slug, items), priceCatKb(slug));
    await ack();

  } else if (d.startsWith("price:add:")) {
    const slug = d.split(":")[2];
    await env.STATE.put(`pending:${userId}`, JSON.stringify({ action: "add", slug }), { expirationTtl: 1800 });
    await send(env, chatId,
      `➕ Новая услуга в «${CATEGORY_RU[slug]}».\nНапиши одной строкой:\n` +
      "<code>Название | цена | время | описание</code>\n(время и описание можно не писать, например: <code>Френч премиум | 150</code>)");
    await ack();

  } else if (d === "photo:cats") {
    await edit(env, chatId, msgId, "📸 В какую галерею добавлять фото?", catGrid("photo:cat"));
    await ack();

  } else if (d.startsWith("photo:cat:")) {
    const slug = d.split(":")[2];
    await env.STATE.put(`photocat:${userId}`, slug, { expirationTtl: 3600 });
    await edit(env, chatId, msgId,
      `📸 Категория «${CATEGORY_RU[slug]}» включена на 1 час — просто присылай фото, подпись не нужна.\n` +
      "Сменить категорию — снова через меню.", MAIN_KB);
    await ack();

  } else if (d === "reviews:ask") {
    await env.STATE.put(`pending:${userId}`, JSON.stringify({ action: "reviews" }), { expirationTtl: 1800 });
    await send(env, chatId, "⭐ Напиши новое число отзывов (например <code>1300</code>):");
    await ack();

  } else if (d === "masters:list") {
    const { data } = await getSiteData(env);
    await edit(env, chatId, msgId, "👩‍🎨 Мастера:", masterListKb(data.masters || []));
    await ack();

  } else if (d === "masters:add") {
    await env.STATE.put(`pending:${userId}`, JSON.stringify({ action: "newmaster" }), { expirationTtl: 1800 });
    await send(env, chatId, "➕ Новый мастер. Напиши одной строкой:\n<code>Имя | Роль</code>\nнапример: <code>Ольга | Manicure i pedicure</code>\n(роль лучше по-польски — она видна на сайте)");
    await ack();

  } else if (d.startsWith("masters:view:")) {
    const slug = d.split(":")[2];
    const { data } = await getSiteData(env);
    const m = (data.masters || []).find(x => x.slug === slug);
    if (!m) { await ack("Не найден"); return; }
    await edit(env, chatId, msgId, masterText(m), masterKb(slug));
    await ack();

  } else if (d.startsWith("masters:srvt:")) {
    const [, , slug, cat] = d.split(":");
    const key = `srvdraft:${userId}:${slug}`;
    let draft = JSON.parse((await env.STATE.get(key)) || "null");
    if (!draft) {
      const { data } = await getSiteData(env);
      draft = ((data.masters || []).find(x => x.slug === slug) || {}).serves || [];
    }
    draft = draft.includes(cat) ? draft.filter(x => x !== cat) : [...draft, cat];
    await env.STATE.put(key, JSON.stringify(draft), { expirationTtl: 1800 });
    await edit(env, chatId, msgId, "✏️ Отметь услуги мастера и нажми «Сохранить»:", servesKb(slug, draft));
    await ack();

  } else if (d.startsWith("masters:srvs:")) {
    const slug = d.split(":")[2];
    const key = `srvdraft:${userId}:${slug}`;
    const draft = JSON.parse((await env.STATE.get(key)) || "null");
    const { data, sha } = await getSiteData(env);
    const m = (data.masters || []).find(x => x.slug === slug);
    if (!m) { await ack("Не найден"); return; }
    if (draft) {
      m.serves = draft;
      await putSiteData(env, data, sha, `Bot: usługi mistrzyni ${m.name}`);
      await env.STATE.delete(key);
    }
    await edit(env, chatId, msgId, `✅ Сохранено. Сайт обновится через ~2 минуты.\n\n` + masterText(m), masterKb(slug));
    await ack();

  } else if (d.startsWith("masters:srv:")) {
    const slug = d.split(":")[2];
    const { data } = await getSiteData(env);
    const m = (data.masters || []).find(x => x.slug === slug);
    if (!m) { await ack("Не найден"); return; }
    await env.STATE.put(`srvdraft:${userId}:${slug}`, JSON.stringify(m.serves || []), { expirationTtl: 1800 });
    await edit(env, chatId, msgId, "✏️ Отметь услуги мастера и нажми «Сохранить»:", servesKb(slug, m.serves || []));
    await ack();

  } else if (d.startsWith("masters:role:")) {
    const slug = d.split(":")[2];
    await env.STATE.put(`pending:${userId}`, JSON.stringify({ action: "role", slug }), { expirationTtl: 1800 });
    await send(env, chatId, "✏️ Напиши новую роль (видна на сайте, лучше по-польски), например: <code>Manicure i stylizacja brwi</code>");
    await ack();

  } else if (d.startsWith("masters:bio:")) {
    const slug = d.split(":")[2];
    await env.STATE.put(`pending:${userId}`, JSON.stringify({ action: "bio", slug }), { expirationTtl: 1800 });
    await send(env, chatId, "✏️ Напиши описание мастера (можно несколько абзацев — раздели пустой строкой):");
    await ack();

  } else if (d.startsWith("masters:photo:")) {
    const slug = d.split(":")[2];
    await env.STATE.put(`pending:${userId}`, JSON.stringify({ action: "masterphoto", slug }), { expirationTtl: 1800 });
    await send(env, chatId, "📷 Пришли фото мастера (портрет, вертикальное лучше):");
    await ack();

  } else if (d.startsWith("masters:del:")) {
    const slug = d.split(":")[2];
    const { data } = await getSiteData(env);
    const m = (data.masters || []).find(x => x.slug === slug);
    if (!m) { await ack("Не найден"); return; }
    await edit(env, chatId, msgId, `Удалить мастера «${m.name}» с сайта?`, {
      inline_keyboard: [[
        { text: "❌ Да, удалить", callback_data: `masters:delok:${slug}` },
        { text: "Отмена", callback_data: `masters:view:${slug}` },
      ]],
    });
    await ack();

  } else if (d.startsWith("masters:delok:")) {
    const slug = d.split(":")[2];
    const { data, sha } = await getSiteData(env);
    const i = (data.masters || []).findIndex(x => x.slug === slug);
    if (i < 0) { await ack("Не найден"); return; }
    const [removed] = data.masters.splice(i, 1);
    await putSiteData(env, data, sha, `Bot: usunięta mistrzyni ${removed.name}`);
    await edit(env, chatId, msgId, `✅ «${removed.name}» удалена с сайта. Обновится через ~2 минуты.`, masterListKb(data.masters));
    await ack();

  } else {
    await ack();
  }
}

// ---------- wiadomości ----------

async function handleMessage(msg, env) {
  const userId = msg.from.id;
  const chatId = msg.chat.id;
  const text = (msg.text || msg.caption || "").trim();

  let admins = JSON.parse((await env.STATE.get("admins")) || "[]");
  if (admins.length === 0) {
    admins = [userId];
    await env.STATE.put("admins", JSON.stringify(admins));
    await send(env, chatId, "Ты назначен администратором этого бота. 👑");
  }
  if (!admins.includes(userId)) {
    await send(env, chatId, `⛔ Нет доступа. Твой ID: ${userId} — попроси администратора добавить тебя.`);
    return;
  }

  if (msg.photo) {
    const pendingRaw = await env.STATE.get(`pending:${userId}`);
    const pending = pendingRaw ? JSON.parse(pendingRaw) : null;
    if (pending && pending.action === "masterphoto") {
      await env.STATE.delete(`pending:${userId}`);
      await handleMasterPhoto(msg, pending.slug, env, chatId);
    } else {
      await handlePhoto(msg, text, env, chatId, userId);
    }
    return;
  }

  // czy czekamy na wpis po naciśnięciu przycisku?
  const pendingRaw = await env.STATE.get(`pending:${userId}`);
  if (pendingRaw && text && !text.startsWith("/")) {
    await env.STATE.delete(`pending:${userId}`);
    await handlePending(JSON.parse(pendingRaw), text, env, chatId);
    return;
  }

  const low = text.toLowerCase().replace(/^\//, "");
  if (low.startsWith("отзыв") || low.startsWith("opinie")) {
    await handleReviews(text, env, chatId);
  } else if (low.startsWith("цены") || low.startsWith("прайс")) {
    await handlePriceList(text, env, chatId);
  } else if (low.startsWith("цена")) {
    await handlePriceSet(text, env, chatId);
  } else if (low.startsWith("услуга")) {
    await handleServiceAdd(text, env, chatId);
  } else if (low.startsWith("удалить")) {
    await handleServiceDelete(text, env, chatId);
  } else if (low.startsWith("разрешить") || low.startsWith("allow")) {
    const m = text.match(/\d{5,}/);
    if (m) {
      admins.push(Number(m[0]));
      await env.STATE.put("admins", JSON.stringify(admins));
      await send(env, chatId, `✅ Пользователь ${m[0]} добавлен.`);
    } else {
      await send(env, chatId, "Напиши так: <code>разрешить 123456789</code>");
    }
  } else {
    await send(env, chatId, HELP, MAIN_KB);
  }
}

async function handlePending(pending, text, env, chatId) {
  if (pending.action === "newmaster") {
    const parts = text.split("|").map(s => s.trim());
    const name = parts[0];
    const role = parts[1] || "";
    if (!name || !role) {
      await send(env, chatId, "Нужно имя и роль через |, например: <code>Ольга | Manicure i pedicure</code>. Попробуй ещё раз через меню.");
      return;
    }
    const { data, sha } = await getSiteData(env);
    data.masters = data.masters || [];
    const slug = translitSlug(name, data.masters.map(m => m.slug));
    const m = { slug, name, gen: name, role, serves: [], bio: [] };
    data.masters.push(m);
    await putSiteData(env, data, sha, `Bot: nowa mistrzyni ${name}`);
    await send(env, chatId,
      `✅ Мастер «${name}» добавлен. Теперь отметь услуги и пришли фото:`, masterKb(slug));
  } else if (pending.action === "role") {
    const { data, sha } = await getSiteData(env);
    const m = (data.masters || []).find(x => x.slug === pending.slug);
    if (!m) { await send(env, chatId, "Мастер не найден."); return; }
    const old = m.role;
    m.role = text;
    await putSiteData(env, data, sha, `Bot: rola ${m.name}: ${text}`);
    await send(env, chatId, `✅ Роль «${m.name}»: ${old} → <b>${text}</b>. Сайт обновится через ~2 минуты.`, masterKb(m.slug));
  } else if (pending.action === "bio") {
    const { data, sha } = await getSiteData(env);
    const m = (data.masters || []).find(x => x.slug === pending.slug);
    if (!m) { await send(env, chatId, "Мастер не найден."); return; }
    m.bio = text.split(/\n\s*\n/).map(s => s.replace(/\s*\n\s*/g, " ").trim()).filter(Boolean);
    await putSiteData(env, data, sha, `Bot: bio ${m.name}`);
    await send(env, chatId, `✅ Описание «${m.name}» обновлено (${m.bio.length} абз.). Сайт обновится через ~2 минуты.`, masterKb(m.slug));
  } else if (pending.action === "reviews") {
    await handleReviews("отзывы " + text, env, chatId);
  } else if (pending.action === "price") {
    const price = normalizePrice(text);
    if (!price) { await send(env, chatId, "Не поняла цену. Например: <code>120</code> или <code>от 120</code>"); return; }
    const { data, sha } = await getSiteData(env);
    const it = (data.services[pending.slug] || [])[pending.idx - 1];
    if (!it) { await send(env, chatId, "Услуга не найдена — открой прайс заново."); return; }
    const old = it[3];
    it[3] = price;
    await putSiteData(env, data, sha, `Bot: cena "${it[0]}" ${old} -> ${price}`);
    await send(env, chatId, `✅ «${it[0]}»: ${old} → <b>${price}</b>. Сайт обновится через ~2 минуты.`, MAIN_KB);
  } else if (pending.action === "add") {
    const parts = text.split("|").map(s => s.trim());
    const name = parts[0];
    const price = parts[1] ? normalizePrice(parts[1]) : null;
    if (!name || !price) {
      await send(env, chatId, "Нужно минимум название и цена: <code>Название | 120</code>. Попробуй ещё раз через меню.");
      return;
    }
    const { data, sha } = await getSiteData(env);
    (data.services[pending.slug] = data.services[pending.slug] || []).push([name, parts[3] || "", parts[2] || "", price]);
    await putSiteData(env, data, sha, `Bot: nowa usługa "${name}" (${pending.slug})`);
    await send(env, chatId, `✅ Добавлена «${name}» — ${price} в «${CATEGORY_RU[pending.slug]}». Сайт обновится через ~2 минуты.`, MAIN_KB);
  }
}

// ---------- zdjęcia ----------

async function handlePhoto(msg, caption, env, chatId, userId) {
  let slug = caption ? CATEGORY_ALIASES[caption.toLowerCase().replace(/^[/#]+/, "").trim()] : null;
  const group = msg.media_group_id;
  if (!slug && group) {
    // album: podpis ma tylko pierwsze zdjęcie — reszta bierze kategorię z KV
    for (let i = 0; i < 6 && !slug; i++) {
      slug = await env.STATE.get(`album:${group}`);
      if (!slug) await new Promise(r => setTimeout(r, 500));
    }
  }
  if (!slug) slug = await env.STATE.get(`photocat:${userId}`); // kategoria z panelu
  if (!slug) {
    await send(env, chatId, `Не поняла категорию. Подпиши фото одним словом (${CATEGORY_LIST}) или выбери её в меню:`, MAIN_KB);
    return;
  }
  if (group) await env.STATE.put(`album:${group}`, slug, { expirationTtl: 3600 });

  const photo = msg.photo.reduce((a, b) => ((a.file_size || 0) > (b.file_size || 0) ? a : b));
  const info = await tg(env, "getFile", { file_id: photo.file_id });
  const fileResp = await fetch(`https://api.telegram.org/file/bot${env.TELEGRAM_TOKEN}/${info.result.file_path}`);
  const bytes = new Uint8Array(await fileResp.arrayBuffer());

  let bin = "";
  const CHUNK = 0x8000;
  for (let i = 0; i < bytes.length; i += CHUNK)
    bin += String.fromCharCode(...bytes.subarray(i, i + CHUNK));

  const path = `assets/gallery/${slug}/tg-${msg.message_id}.jpg`;
  await gh(env, `contents/${path}`, "PUT", {
    message: `Bot: nowe zdjęcie w galerii ${slug}`,
    content: btoa(bin),
  });
  await send(env, chatId, `✅ Фото добавлено в галерею «${CATEGORY_RU[slug] || slug}». Сайт обновится через ~2 минуты.`);
}

async function downloadPhotoB64(msg, env) {
  const photo = msg.photo.reduce((a, b) => ((a.file_size || 0) > (b.file_size || 0) ? a : b));
  const info = await tg(env, "getFile", { file_id: photo.file_id });
  const fileResp = await fetch(`https://api.telegram.org/file/bot${env.TELEGRAM_TOKEN}/${info.result.file_path}`);
  const bytes = new Uint8Array(await fileResp.arrayBuffer());
  let bin = "";
  const CHUNK = 0x8000;
  for (let i = 0; i < bytes.length; i += CHUNK)
    bin += String.fromCharCode(...bytes.subarray(i, i + CHUNK));
  return btoa(bin);
}

async function handleMasterPhoto(msg, slug, env, chatId) {
  const path = `assets/mistrz-${slug}.jpg`;
  let sha;
  try { sha = (await gh(env, `contents/${path}`, "GET")).sha; } catch {}
  await gh(env, `contents/${path}`, "PUT", {
    message: `Bot: zdjęcie mistrzyni ${slug}`,
    content: await downloadPhotoB64(msg, env),
    ...(sha ? { sha } : {}),
  });
  await send(env, chatId, `✅ Фото мастера сохранено. Сайт обновится через ~2 минуты.`, masterKb(slug));
}

// ---------- opinie ----------

async function handleReviews(text, env, chatId) {
  const m = text.match(/\d{2,6}/);
  if (!m) {
    await send(env, chatId, "Напиши так: <code>отзывы 1300</code>");
    return;
  }
  const n = Number(m[0]);
  const { data, sha } = await getSiteData(env);
  if (data.reviews === n) {
    await send(env, chatId, `Число отзывов уже ${n} — ничего не меняю.`);
    return;
  }
  data.reviews = n;
  await putSiteData(env, data, sha, `Bot: liczba opinii ${n}`);
  await send(env, chatId, `✅ Число отзывов обновлено: ${n}. Сайт обновится через ~2 минуты.`, MAIN_KB);
}

// ---------- cennik: komendy tekstowe ----------

async function getSiteData(env) {
  const cur = await gh(env, "contents/site_data.json", "GET");
  const bytes = Uint8Array.from(atob(cur.content.replace(/\n/g, "")), c => c.charCodeAt(0));
  return { data: JSON.parse(new TextDecoder().decode(bytes)), sha: cur.sha };
}

async function putSiteData(env, data, sha, message) {
  const bytes = new TextEncoder().encode(JSON.stringify(data, null, 1) + "\n");
  let bin = "";
  for (const b of bytes) bin += String.fromCharCode(b);
  await gh(env, "contents/site_data.json", "PUT", { message, content: btoa(bin), sha });
}

function parseCategoryArg(text) {
  const parts = text.trim().split(/\s+/);
  const slug = parts.length > 1 ? CATEGORY_ALIASES[parts[1].toLowerCase()] : null;
  return { slug, rest: parts.slice(2) };
}

function normalizePrice(raw) {
  const s = raw.trim();
  if (/zł/i.test(s)) return s;
  const od = /^(от|od)[\s\d]/i.test(s);
  const num = (s.match(/\d+/) || [null])[0];
  if (!num) return null;
  return (od ? "od " : "") + num + " zł";
}

async function handlePriceList(text, env, chatId) {
  const { slug } = parseCategoryArg(text);
  if (!slug) {
    await send(env, chatId, "💰 Выбери категорию:", catGrid("price:cat"));
    return;
  }
  const { data } = await getSiteData(env);
  await send(env, chatId, priceListText(slug, data.services[slug] || []), priceCatKb(slug));
}

async function handlePriceSet(text, env, chatId) {
  const { slug, rest } = parseCategoryArg(text);
  const idx = rest.length ? parseInt(rest[0], 10) : NaN;
  const price = normalizePrice(rest.slice(1).join(" "));
  if (!slug || !idx || !price) {
    await send(env, chatId, "Напиши так: <code>цена маникюр 3 120</code> или <code>цена маникюр 3 от 120</code>\n(номер услуги смотри через <code>цены маникюр</code>)");
    return;
  }
  const { data, sha } = await getSiteData(env);
  const items = data.services[slug] || [];
  if (idx < 1 || idx > items.length) {
    await send(env, chatId, `В «${slug}» только ${items.length} услуг. Посмотри номера: <code>цены ${slug}</code>`);
    return;
  }
  const old = items[idx - 1][3];
  items[idx - 1][3] = price;
  await putSiteData(env, data, sha, `Bot: cena "${items[idx - 1][0]}" ${old} -> ${price}`);
  await send(env, chatId, `✅ «${items[idx - 1][0]}»: ${old} → <b>${price}</b>. Сайт обновится через ~2 минуты.`);
}

async function handleServiceAdd(text, env, chatId) {
  const { slug } = parseCategoryArg(text);
  const afterCat = text.trim().split(/\s+/).slice(2).join(" ");
  const parts = afterCat.split("|").map(s => s.trim());
  const name = parts[0];
  const price = parts[1] ? normalizePrice(parts[1]) : null;
  if (!slug || !name || !price) {
    await send(env, chatId, "Напиши так: <code>услуга маникюр Название | 120 | 1 г 30 мин | Описание</code>\n(время и описание — по желанию)");
    return;
  }
  const { data, sha } = await getSiteData(env);
  (data.services[slug] = data.services[slug] || []).push([name, parts[3] || "", parts[2] || "", price]);
  await putSiteData(env, data, sha, `Bot: nowa usługa "${name}" (${slug})`);
  await send(env, chatId, `✅ Добавлена услуга «${name}» — ${price} в «${slug}». Сайт обновится через ~2 минуты.`);
}

async function handleServiceDelete(text, env, chatId) {
  const { slug, rest } = parseCategoryArg(text);
  const idx = rest.length ? parseInt(rest[0], 10) : NaN;
  if (!slug || !idx) {
    await send(env, chatId, "Напиши так: <code>удалить маникюр 3</code> (номер — из <code>цены маникюр</code>)");
    return;
  }
  const { data, sha } = await getSiteData(env);
  const items = data.services[slug] || [];
  if (idx < 1 || idx > items.length) {
    await send(env, chatId, `В «${slug}» только ${items.length} услуг.`);
    return;
  }
  const [removed] = items.splice(idx - 1, 1);
  await putSiteData(env, data, sha, `Bot: usunięta usługa "${removed[0]}" (${slug})`);
  await send(env, chatId, `✅ Услуга «${removed[0]}» удалена из «${slug}». Сайт обновится через ~2 минуты.`);
}

// ---------- Telegram / GitHub API ----------

async function tg(env, method, params) {
  const r = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_TOKEN}/${method}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(params),
  });
  const j = await r.json();
  if (!j.ok) throw new Error(`Telegram ${method}: ${j.description}`);
  return j;
}

async function send(env, chatId, text, kb) {
  await tg(env, "sendMessage", { chat_id: chatId, text, parse_mode: "HTML", ...(kb ? { reply_markup: kb } : {}) });
}

async function edit(env, chatId, msgId, text, kb) {
  try {
    await tg(env, "editMessageText", {
      chat_id: chatId, message_id: msgId, text, parse_mode: "HTML",
      ...(kb ? { reply_markup: kb } : {}),
    });
  } catch (e) {
    if (!/message is not modified/.test(e.message)) throw e;
  }
}

async function gh(env, path, method, body) {
  const r = await fetch(`https://api.github.com/repos/${REPO}/${path}`, {
    method,
    headers: {
      "Authorization": `Bearer ${env.GH_TOKEN}`,
      "User-Agent": "badangel-bot",
      "Accept": "application/vnd.github+json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!r.ok) throw new Error(`GitHub ${method} ${path}: ${r.status} ${(await r.text()).slice(0, 200)}`);
  return r.json();
}
