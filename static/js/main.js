document.getElementById('scan-btn').addEventListener('click', async () => {
    const url = document.getElementById('url-input').value;
    const resultsDiv = document.getElementById('results');

    if (!url) return;

    // Visual feedback that scan is happening
    resultsDiv.classList.remove('hidden');
    resultsDiv.innerHTML = "<p>POLLING HEURISTIC ENGINE...</p>";
    resultsDiv.className = "results-box"; 

    try {
        const response = await fetch('/scan', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        const data = await response.json();
        
        // Apply SOC risk styling
        resultsDiv.classList.add(data.level.toLowerCase());
        
        resultsDiv.innerHTML = `
            <h2>THREAT LEVEL: ${data.level}</h2>
            <p>Risk Score: ${data.score}/100</p>
            <hr style="border: 0; border-top: 1px dashed #444; margin: 10px 0;">
            <ul>
                ${data.findings.map(f => `<li>${f}</li>`).join('')}
            </ul>
        `;
    } catch (error) {
        resultsDiv.innerHTML = "<p>ERROR: CONNECTION TO ENGINE TIMED OUT.</p>";
    }
});