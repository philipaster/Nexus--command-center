const $=id=>document.getElementById(id);
function clock(){ $('clock').textContent=new Date().toLocaleTimeString(); } setInterval(clock,1000); clock();

async function refreshStats(){
 const r=await fetch('/api/stats'); const s=await r.json();
 $('taskCount').textContent=s.tasks; $('doneCount').textContent=s.completed; $('noteCount').textContent=s.notes;
}
async function loadTasks(){
 const r=await fetch('/api/stats'); await r.json();
 // Server-rendered initial tasks are replaced through a lightweight page refresh after mutations.
}
async function addTask(){
 const title=$('taskInput').value.trim(); if(!title)return;
 await fetch('/api/tasks',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title})});
 $('taskInput').value=''; location.reload();
}
async function toggleTask(id){await fetch('/api/tasks/'+id,{method:'PATCH'});location.reload()}
async function deleteTask(id){await fetch('/api/tasks/'+id,{method:'DELETE'});location.reload()}
async function addNote(){
 const title=$('noteTitle').value.trim(),body=$('noteBody').value.trim(); if(!title||!body)return;
 await fetch('/api/notes',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({title,body})});
 location.reload();
}
async function deleteNote(id){await fetch('/api/notes/'+id,{method:'DELETE'});location.reload()}
async function genPassword(){
 const len=prompt("Password length (8-64):","20")||20;
 const r=await fetch('/api/generate-password?length='+encodeURIComponent(len));
 $('password').value=(await r.json()).password;
}
async function copyPassword(){
 if(!$('password').value)return;
 await navigator.clipboard.writeText($('password').value);
 const old=$('.ghost').textContent; $('.ghost').textContent='COPIED ✓';
 setTimeout(()=>$('.ghost').textContent=old,1200);
}
refreshStats();

document.addEventListener('keydown',e=>{
 if(e.key==='Enter' && document.activeElement===$('taskInput')) addTask();
});
