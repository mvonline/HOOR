import React,{useCallback,useEffect,useRef,useState} from 'react';
import {X,ChevronLeft,ChevronRight,RotateCcw,RotateCw,Maximize2,Play} from 'lucide-react';

export type Clip={n:number;title:string;note:string;rot:number;mins:string};
// rot = degrees the footage must be turned to stand upright (the files were shot or exported sideways).
export const CLIPS:Clip[]=[
 {n:0,title:'شکاف از بالا',note:'کاروان در دلِ شکاف، از ارتفاع',rot:0,mins:'۰:۲۴'},
 {n:1,title:'چادرگاه زیر صخره',note:'خودروها در پناهِ دیواره، نمای عمودی',rot:90,mins:'۰:۲۶'},
 {n:2,title:'مرزِ دشت و تنگه',note:'خطِ تیرهٔ شکاف در بیابان بی‌انتها',rot:90,mins:'۱:۲۳'},
 {n:3,title:'کاروان در شیار',note:'از داخلِ خودرو، میان دیواره‌ها',rot:0,mins:'۱:۲۸'},
 {n:4,title:'مسیر باریک',note:'ردِ خودروها در کفِ شکاف',rot:0,mins:'۰:۲۰'},
 {n:5,title:'آدم‌ها در کفِ ترک‌خورده',note:'مقیاسِ آدم در برابر دیواره',rot:0,mins:'۰:۴۱'},
 {n:6,title:'دیوارهٔ لایه‌لایه',note:'لایه‌های رسوبی و لبهٔ شکاف',rot:0,mins:'۰:۲۷'},
 {n:7,title:'راهِ شنی',note:'خاکِ نرم و ردِ لاستیک',rot:0,mins:'۰:۱۷'},
 {n:8,title:'گذر از تنگه',note:'عبور از میان دیواره‌های تنگ',rot:0,mins:'۳:۲۶'},
 {n:9,title:'تپه‌های ماسه',note:'ماسه و آسمان، پیش از غروب',rot:-90,mins:'۰:۴۸'},
 {n:10,title:'غبارِ غروب',note:'نورِ نارنجی بر جادهٔ خاکی',rot:0,mins:'۰:۰۹'},
];
const url=(f:string)=>new URL('./media/tango/'+f,document.baseURI).pathname;
const faNum=(n:number)=>n.toLocaleString('fa-IR');

function Player({start,onClose}:{start:number;onClose:()=>void}){
 const [i,setI]=useState(start);
 const [extra,setExtra]=useState<Record<number,number>>({});
 const box=useRef<HTMLDivElement>(null);
 const clip=CLIPS[i];
 const deg=(clip.rot+(extra[clip.n]||0)+360*8)%360;
 const turned=deg===90||deg===270;
 const go=useCallback((d:number)=>setI(x=>(x+d+CLIPS.length)%CLIPS.length),[]);
 const rotate=(d:number)=>setExtra(e=>({...e,[clip.n]:((e[clip.n]||0)+d+360)%360}));
 const full=()=>{const el=box.current;if(!el)return;try{if(document.fullscreenElement)document.exitFullscreen();else el.requestFullscreen?.();}catch{}};
 useEffect(()=>{
  const key=(e:KeyboardEvent)=>{
   if(e.key==='Escape')onClose();
   else if(e.key==='ArrowRight')go(-1); // RTL page: right = previous
   else if(e.key==='ArrowLeft')go(1);
   else if(e.key==='r'||e.key==='R')rotate(e.shiftKey?-90:90);
   else if(e.key==='f'||e.key==='F')full();
  };
  addEventListener('keydown',key);const prev=document.body.style.overflow;document.body.style.overflow='hidden';
  return()=>{removeEventListener('keydown',key);document.body.style.overflow=prev;};
 });
 const stage:React.CSSProperties=turned
  ?{width:'100vh',height:'100vw',transform:`translate(-50%,-50%) rotate(${deg}deg)`}
  :{width:'100vw',height:'100vh',transform:`translate(-50%,-50%) rotate(${deg}deg)`};
 return <div className="tg-player" ref={box} role="dialog" aria-label={`ویدیو ${faNum(clip.n)}: ${clip.title}`}>
  <div className="tg-stage" style={stage}><video key={clip.n} src={url(clip.n+'.mp4')} controls autoPlay playsInline preload="metadata" onEnded={()=>go(1)}/></div>
  <div className="tg-bar top"><button onClick={onClose} aria-label="بستن"><X size={22}/></button><div className="tg-title"><strong>{faNum(clip.n)} · {clip.title}</strong><small>{faNum(i+1)} از {faNum(CLIPS.length)}</small></div></div>
  <div className="tg-bar side">
   <button onClick={()=>go(1)} aria-label="بعدی"><ChevronLeft size={26}/></button>
   <button onClick={()=>go(-1)} aria-label="قبلی"><ChevronRight size={26}/></button>
  </div>
  <div className="tg-bar bottom">
   <button onClick={()=>rotate(-90)} title="چرخش ۹۰ درجه به چپ (Shift+R)"><RotateCcw size={20}/>چپ</button>
   <button onClick={()=>rotate(90)} title="چرخش ۹۰ درجه به راست (R)"><RotateCw size={20}/>راست</button>
   <button onClick={full} title="تمام‌صفحه (F)"><Maximize2 size={20}/>تمام‌صفحه</button>
  </div>
 </div>;
}

export default function TangoPage(){
 const [open,setOpen]=useState<number|null>(null);
 return <section className="section tg-page">
  <span className="eyebrow">معرفی</span>
  <h1>تنگهٔ رتیل</h1>
  <p className="tg-lead">تنگه رتیل در دل بیابان سوزان لوت، شکافی رازآلود و باشکوه است؛ جایی که سکوت عمیق کویر، با غرور صخره‌ها و رد پای زمان در هم می‌آمیزد. این تنگه خشن و تماشایی، یادآور قدرت بی‌رحم اما زیبای طبیعت است؛ جایی که هر قدم، احترام به عظمت زمین و گذر قرن‌ها را زمزمه می‌کند.</p>
  <div className="tg-meta"><span>{faNum(CLIPS.length)} ویدیو</span><span>پخش‌کننده تمام‌صفحه است و هر ویدیو را می‌شود ۹۰ درجه چرخاند</span></div>
  <ol className="tg-grid">
   {CLIPS.map((c,k)=><li key={c.n}>
    <button className="tg-card" onClick={()=>setOpen(k)} aria-label={`پخش ویدیو ${faNum(c.n)}: ${c.title}`}>
     <span className="tg-thumb"><img src={url('p'+c.n+'.jpg')} alt="" loading="lazy"/><span className="tg-play"><Play size={26}/></span><span className="tg-idx">{faNum(c.n)}</span><span className="tg-dur">{c.mins}</span></span>
     <span className="tg-cap"><strong>{c.title}</strong><small>{c.note}</small></span>
    </button>
   </li>)}
  </ol>
  <p className="tg-credit">برخی تصاویر مهرِ سازندگانشان را دارند؛ حقوقِ ویدیوها متعلق به صاحبان آن‌هاست و اینجا فقط برای مطالعهٔ فضای داستان نمایش داده می‌شوند.</p>
  {open!==null&&<Player start={open} onClose={()=>setOpen(null)}/>}
 </section>;
}
