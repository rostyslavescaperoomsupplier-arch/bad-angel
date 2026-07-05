// Auto-generowane przez build.py — funkcje interaktywne.
(function(){
  "use strict";
  var $ = function(s,r){return (r||document).querySelector(s);};
  var $$ = function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));};
  var visibleGallery = function(){ return $$(".gallery img").filter(function(im){return im.offsetParent!==null;}); };

  document.addEventListener("DOMContentLoaded", function(){
    reveal(); toTop(); faq(); lightbox(); calc(); filter(); beforeAfter(); share();
  });

  function reveal(){
    var els=$$(".reveal");
    if(!("IntersectionObserver" in window)){ els.forEach(function(e){e.classList.add("in");}); return; }
    var io=new IntersectionObserver(function(en){ en.forEach(function(x){ if(x.isIntersecting){ x.target.classList.add("in"); io.unobserve(x.target); } }); }, {threshold:0.12, rootMargin:"0px 0px -8% 0px"});
    els.forEach(function(e){ io.observe(e); });
  }

  function toTop(){
    var b=$("#toTop"); if(!b) return;
    addEventListener("scroll", function(){ b.classList.toggle("show", scrollY>500); });
    b.addEventListener("click", function(){ scrollTo({top:0, behavior:"smooth"}); });
  }

  function faq(){
    $$(".faq-item").forEach(function(it){
      var q=$(".faq-q",it), a=$(".faq-a",it);
      q.addEventListener("click", function(){ var o=it.classList.toggle("open"); a.style.maxHeight=o?a.scrollHeight+"px":"0"; });
    });
  }

  function lightbox(){
    var lb=$("#lightbox"); if(!lb) return;
    var img=$("#lbImg"), list=[], idx=0;
    function show(){ if(list[idx]) img.src=list[idx].src; }
    function open(i){ list=visibleGallery(); idx=i; show(); lb.classList.add("open"); document.body.style.overflow="hidden"; }
    function close(){ lb.classList.remove("open"); document.body.style.overflow=""; }
    function nav(d){ if(!list.length)return; idx=(idx+d+list.length)%list.length; show(); }
    document.addEventListener("click", function(e){
      var t=e.target; if(t.matches && t.matches(".gallery img")){ open(visibleGallery().indexOf(t)); }
    });
    $(".lb-close",lb).addEventListener("click", close);
    $(".lb-prev",lb).addEventListener("click", function(e){ e.stopPropagation(); nav(-1); });
    $(".lb-next",lb).addEventListener("click", function(e){ e.stopPropagation(); nav(1); });
    lb.addEventListener("click", function(e){ if(e.target===lb) close(); });
    addEventListener("keydown", function(e){ if(!lb.classList.contains("open"))return; if(e.key==="Escape")close(); else if(e.key==="ArrowLeft")nav(-1); else if(e.key==="ArrowRight")nav(1); });
  }

  function calc(){
    var box=$("#calc"); if(!box) return;
    var sumEl=$("#calcSum"), cntEl=$("#calcCount");
    function upd(){
      var s=0,n=0,from=false;
      $$("input[type=checkbox]",box).forEach(function(c){ if(c.checked){ s+=parseFloat(c.getAttribute("data-price"))||0; n++; if(c.getAttribute("data-from")==="1")from=true; } });
      sumEl.textContent=(from&&n?"od ":"")+Math.round(s)+" zł"; cntEl.textContent=n;
    }
    box.addEventListener("change", upd);
    var clr=$("#calcClear"); if(clr) clr.addEventListener("click", function(){ $$("input[type=checkbox]",box).forEach(function(c){c.checked=false;}); upd(); });
    upd();
  }

  function filter(){
    var f=$("#pfFilters"); if(!f) return;
    f.addEventListener("click", function(e){
      var b=e.target.closest("button"); if(!b) return;
      $$("button",f).forEach(function(x){x.classList.remove("active");}); b.classList.add("active");
      var flt=b.getAttribute("data-filter");
      $$("#pfGrid img").forEach(function(im){ im.classList.toggle("hide", flt!=="all" && im.getAttribute("data-cat")!==flt); });
    });
  }

  function beforeAfter(){
    var ba=$("#baSlider"); if(!ba) return;
    var after=$(".ba-after",ba), line=$(".ba-line",ba), handle=$(".ba-handle",ba), drag=false;
    function set(p){ p=Math.max(0,Math.min(100,p)); after.style.clipPath="inset(0 0 0 "+p+"%)"; line.style.left=p+"%"; handle.style.left=p+"%"; }
    function fromX(x){ var r=ba.getBoundingClientRect(); set((x-r.left)/r.width*100); }
    ba.addEventListener("pointerdown", function(e){ drag=true; fromX(e.clientX); try{ba.setPointerCapture(e.pointerId);}catch(_){} });
    ba.addEventListener("pointermove", function(e){ if(drag){ e.preventDefault(); fromX(e.clientX); } });
    addEventListener("pointerup", function(){ drag=false; });
    set(50);
  }

  function share(){
    var url=location.origin+location.pathname.replace(/[^/]*$/,"")||location.href;
    var text="Salon Urody BAD ANGEL — Szczecin";
    var map={ wa:"https://wa.me/?text="+encodeURIComponent(text+" "+url),
      tg:"https://t.me/share/url?url="+encodeURIComponent(url)+"&text="+encodeURIComponent(text),
      fb:"https://www.facebook.com/sharer/sharer.php?u="+encodeURIComponent(url) };
    $$(".js-share").forEach(function(a){ a.href=map[a.getAttribute("data-net")]||url; });
    $$(".js-copy").forEach(function(b){
      b.addEventListener("click", function(){
        function done(){ var l=window.__lang||"pl", t=window.I18N&&window.I18N.share_copied;
          b.textContent=t?t[l]:"OK";
          setTimeout(function(){ var k=window.I18N&&window.I18N.share_copy; if(k)b.textContent=k[l]; },1600); }
        if(navigator.clipboard){ navigator.clipboard.writeText(url).then(done, function(){ prompt("Link:",url); }); }
        else { prompt("Link:",url); }
      });
    });
  }
})();
