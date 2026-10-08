let chart;
function showMessage(msg){const el=document.getElementById("message");el.style.display="block";el.textContent=msg}
async function startScan(){
 const btn=document.getElementById("scanBtn"), target=document.getElementById("target").value.trim();
 if(!document.getElementById("authorized").checked){showMessage("Please confirm that you own the target or have explicit permission to test it.");return}
 if(!/^https?:\/\//i.test(target)){showMessage("Enter a valid http:// or https:// target.");return}
 btn.disabled=true; btn.textContent="Crawling...";
 showMessage("Starting authorized crawl. Discovering same-origin pages...");
 try{
  const r=await fetch("/api/scan",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
   target, authorized:true, max_pages:document.getElementById("maxPages").value,
   max_depth:document.getElementById("maxDepth").value, delay:0.4
  })});
  const data=await r.json(); if(!r.ok) throw new Error(data.error||"Scan failed");
  document.getElementById("pages").textContent=data.pages_crawled;
  document.getElementById("endpoints").textContent=data.urls_discovered;
  document.getElementById("forms").textContent=data.forms_found;
  const s=data.summary; ["high","medium","low","info"].forEach(x=>document.getElementById(x).textContent=s[x]);
  document.getElementById("total").textContent=s.high+s.medium+s.low+s.info;
  document.getElementById("scanTime").textContent="Completed "+data.finished_at;
  renderChart(s); renderCrawl(data.pages); renderEndpoints(data); renderFindings(data.findings);
  showMessage(`Crawl completed: ${data.pages_crawled} pages fetched and ${data.urls_discovered} URLs discovered.`);
 }catch(e){showMessage("Error: "+e.message)}finally{btn.disabled=false;btn.textContent="Start Crawl & Scan"}
}
function renderCrawl(pages){
 const box=document.getElementById("crawlList");
 if(!pages.length){box.innerHTML='<div class="empty">No pages could be fetched.</div>';return}
 box.innerHTML=pages.map((p,i)=>`<div class="crawl-row"><span class="dot"></span><span class="num">${String(i+1).padStart(2,"0")}</span><span class="url">${escapeHtml(p.url)}</span><span class="depth">depth ${p.depth}</span><span class="code">${p.status}</span></div>`).join("");
}
function renderChart(s){
 if(chart) chart.destroy();
 chart=new Chart(document.getElementById("riskChart"),{type:"doughnut",data:{labels:["High","Medium","Low","Info"],datasets:[{data:[s.high,s.medium,s.low,s.info]}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:"bottom",labels:{color:"#9eb2c8"}}}}});
}
function renderEndpoints(data){
 const body=document.getElementById("endpointTable");body.innerHTML="";
 data.pages.forEach(p=>{const tr=document.createElement("tr");tr.innerHTML=`<td>${escapeHtml(p.url)}</td><td>${p.status}</td><td>${p.depth}</td><td>${escapeHtml(p.content_type||"")}</td>`;body.appendChild(tr)});
}
function renderFindings(items){
 const box=document.getElementById("findings");
 if(!items.length){box.innerHTML='<div class="empty">No findings detected by the current checks.</div>';return}
 box.innerHTML=items.map(f=>`<div class="finding"><div class="finding-top"><b>${escapeHtml(f.type)}</b><span class="sev ${f.severity.toUpperCase()}">${f.severity.toUpperCase()}</span></div><p>${escapeHtml(f.evidence)}</p><small>Recommended action: ${escapeHtml(f.action)}</small><br><small>URL: ${escapeHtml(f.url)}</small></div>`).join("");
}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]))}
function downloadReport(){window.location="/report"}
