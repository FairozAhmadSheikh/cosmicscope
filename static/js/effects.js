// Starfield background
const canvas = document.createElement('canvas');
document.body.appendChild(canvas);
canvas.style.position = 'fixed';
canvas.style.top = 0;
canvas.style.left = 0;
canvas.style.width = '100%';
canvas.style.height = '100%';
canvas.style.zIndex = '-1';
const ctx = canvas.getContext('2d');

let stars = [];
function initStars() {
  stars = [];
  for(let i=0;i<200;i++){
    stars.push({
      x: Math.random()*window.innerWidth,
      y: Math.random()*window.innerHeight,
      r: Math.random()*1.5,
      d: Math.random()*0.5
    });
  }
}
function drawStars() {
  ctx.clearRect(0,0,canvas.width,canvas.height);
  for(let s of stars){
    ctx.beginPath();
    ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
    ctx.fillStyle = 'white';
    ctx.fill();
  }
}
function animateStars() {
  for(let s of stars){
    s.y += 0.2 + s.d;
    if(s.y > window.innerHeight) s.y=0;
  }
  drawStars();
  requestAnimationFrame(animateStars);
}
function resizeCanvas() {
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  initStars();
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();
animateStars();

// Modal + GPT-4 fetch
const modal = document.getElementById('insight-modal');
const modalImg = document.getElementById('modal-img');
const modalTitle = document.getElementById('modal-title');
const modalDate = document.getElementById('modal-date');
const modalInsight = document.getElementById('modal-insight');
const closeBtn = modal.querySelector('.close');

document.querySelectorAll('.card').forEach(card=>{
  card.addEventListener('click', async ()=>{
    modal.style.display='flex';
    modalImg.src = card.querySelector('img').src;
    modalTitle.innerText = card.dataset.title;
    modalDate.innerText = card.dataset.date;
    modalInsight.innerText = 'Loading insight...';

    // Fetch insight
    const resp = await fetch('/get_insight',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({
        title: card.dataset.title,
        date: card.dataset.date,
        explanation: card.dataset.explanation
      })
    });
    const data = await resp.json();
    modalInsight.innerText = data.insight;
  });
});

closeBtn.addEventListener('click', ()=>{
  modal.style.display='none';
});
