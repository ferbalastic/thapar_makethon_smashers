document.getElementById('analyze-btn').addEventListener('click', async () => {
    const btn = document.getElementById('analyze-btn');
    const loading = document.getElementById('loading');
    const resultBox = document.getElementById('result-box');
    
    // Switch UI to loading state
    btn.style.display = 'none';
    loading.style.display = 'block';
    resultBox.style.display = 'none';

    // 1. Get the current active tab
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    // 2. Inject the scraper script into the page
    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        files: ['content.js']
    }, () => {
        // 3. Ask the scraper for the text
        chrome.tabs.sendMessage(tab.id, { action: "get_page_text" }, async (response) => {
            if (response && response.text) {
                
                // Hardcoded profile for the hackathon demo
                const mockProfile = {
                    name: "Demo Applicant",
                    course: "B.Tech",
                    current_year: "2nd Year",
                    cgpa: 8.5,
                    annual_family_income: 600000,
                    category: "General"
                };

                // 4. Send the scraped text and the profile to your FastAPI backend
                try {
                    const apiRes = await fetch("http://localhost:8000/analyze_website", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            website_text: response.text,
                            profile: mockProfile
                        })
                    });
                    
                    const data = await apiRes.json();
                    
                    // 5. Update the UI with the AI's verdict
                    loading.style.display = 'none';
                    btn.style.display = 'block';
                    resultBox.style.display = 'block';
                    
                    document.getElementById('status-text').innerText = data.status;
                    document.getElementById('status-text').className = `status ${data.status}`;
                    document.getElementById('reason-text').innerText = data.reason;

                } catch (error) {
                    loading.style.display = 'none';
                    btn.style.display = 'block';
                    alert("Error connecting to Scholara. Make sure your FastAPI server is running!");
                }
            }
        });
    });
});