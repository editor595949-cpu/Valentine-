const yesBtn = document.getElementById("yesBtn");
const noBtn = document.getElementById("noBtn");
const container = document.getElementById("container");
const loveMessage = document.getElementById("loveMessage");

/* ---------- SAFE MOVE ---------- */
function moveNoButton(){
    const yesRect = yesBtn.getBoundingClientRect();
    const containerRect = container.getBoundingClientRect();

    let x,y,safe=false;

    while(!safe){
        x=Math.random()*(containerRect.width-100);
        y=Math.random()*(containerRect.height+200);

        const absX=containerRect.left+x;
        const absY=containerRect.top+y;

        const overlapYes=
            absX<yesRect.right &&
            absX+100>yesRect.left &&
            absY<yesRect.bottom &&
            absY+40>yesRect.top;

        if(!overlapYes) safe=true;
    }

    noBtn.style.position="absolute";
    noBtn.style.left=x+"px";
    noBtn.style.top=y+"px";
}

noBtn.addEventListener("mouseenter",moveNoButton);
noBtn.addEventListener("touchstart",function(e){
    e.preventDefault();
    moveNoButton();
});

/* ---------- FIREWORK ---------- */
function firework(x,y){
    for(let i=0;i<20;i++){
        const p=document.createElement("div");
        p.className="particle";

        const angle=Math.random()*2*Math.PI;
        const distance=Math.random()*120;

        p.style.setProperty("--x",Math.cos(angle)*distance+"px");
        p.style.setProperty("--y",Math.sin(angle)*distance+"px");

        p.style.left=x+"px";
        p.style.top=y+"px";
        p.style.background=["#fff","#ff0","#0ff","#f0f","#0f0"][Math.floor(Math.random()*5)];

        document.body.appendChild(p);
        setTimeout(()=>p.remove(),1000);
    }
}

/* ---------- YES CLICK ---------- */
yesBtn.addEventListener("click",()=>{

    noBtn.style.display="none";

    for(let i=0;i<6;i++){
        firework(
            Math.random()*window.innerWidth,
            Math.random()*window.innerHeight
        );
    }

    yesBtn.innerText="I already know that ❤️";

    loveMessage.innerHTML = 
    "From this moment, it's you and me against the world ❤️<br><br>" +
    "I promise to stand by you, laugh with you, and annoy you forever 😌";

    loveMessage.style.opacity="1";
});