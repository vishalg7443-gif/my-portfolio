document.addEventListener('DOMContentLoaded', () => {
  const previews = {
    'Hello World + AI Chat': `
      <div class="project-preview">
        <div class="preview-label">Flask + AI Chat</div>
        <div class="preview-window">
          <div class="preview-row"><span class="preview-dot"></span><span class="preview-dot"></span><span class="preview-dot"></span></div>
          <div class="chat-stack">
            <div class="chat-bubble">How can AI help me learn faster?</div>
            <div class="chat-bubble ai">Ask a focused question and I’ll help break it down.</div>
            <div class="chat-bubble">Now it feels like a real app.</div>
          </div>
        </div>
      </div>`,
    'My Financial Future Data & Visualization': `
      <div class="project-preview">
        <div class="preview-label">Financial Dashboard</div>
        <div class="preview-window">
          <div class="finance-bars">
            <div class="finance-bar"><span style="width:82%"></span></div>
            <div class="finance-bar"><span style="width:61%"></span></div>
            <div class="finance-bar"><span style="width:93%"></span></div>
          </div>
          <div class="finance-stat"><span>Start at 18</span><strong>More time to compound</strong></div>
          <div class="finance-stat"><span>Start at 28</span><span>Less growth time</span></div>
        </div>
      </div>`,
    'MCP Agent Workflow': `
      <div class="project-preview">
        <div class="preview-label">Agent Tool Workflow</div>
        <div class="preview-window">
          <div class="agent-map">
            <div class="agent-node">User prompt</div><div class="agent-arrow">→</div>
            <div class="agent-node">AI agent</div><div class="agent-arrow">→</div>
            <div class="agent-node">MCP tool</div>
          </div>
        </div>
      </div>`,
    'AI Study Buddy with RAG': `
      <div class="project-preview">
        <div class="preview-label">RAG Study Assistant</div>
        <div class="preview-window">
          <div class="rag-flow">
            <div class="rag-step">PDF<br>upload</div>
            <div class="rag-step">Retrieve<br>context</div>
            <div class="rag-step">Grounded<br>answer</div>
          </div>
          <div class="rag-answer">Question → relevant document chunks → answer based on the source.</div>
        </div>
      </div>`,
    'AI Games: Tic-Tac-Toe & Hangman': `
      <div class="project-preview">
        <div class="preview-label">AI Game Experience</div>
        <div class="preview-window game-preview">
          <div class="tic-grid">
            <div class="tic-cell">X</div><div class="tic-cell">O</div><div class="tic-cell">X</div>
            <div class="tic-cell">O</div><div class="tic-cell">X</div><div class="tic-cell"></div>
            <div class="tic-cell"></div><div class="tic-cell">O</div><div class="tic-cell"></div>
          </div>
          <div class="game-copy">
            <div class="game-pill">AI opponent</div>
            <div class="game-pill">Hints + commentary</div>
            <div class="game-pill">Leaderboard + recap</div>
          </div>
        </div>
      </div>`
  };

  const linkLabels = {
    'MCP Agent Workflow': 'Open MCP code',
    'AI Study Buddy with RAG': 'Open RAG app code',
    'AI Games: Tic-Tac-Toe & Hangman': 'Open game code'
  };

  document.querySelectorAll('.project-card').forEach((card) => {
    const title = card.querySelector('h3')?.textContent.trim();
    const image = card.querySelector('.project-image');
    if (title && image && !image.querySelector('img') && previews[title]) {
      image.innerHTML = previews[title];
      image.setAttribute('aria-label', `Project preview for ${title}`);
    }

    const links = [...card.querySelectorAll('.project-links a')];
    const projectLink = links.find((link) => link.textContent.trim() === 'Project link');
    const githubLink = links.find((link) => link.textContent.trim() === 'GitHub');
    if (projectLink && title) projectLink.textContent = linkLabels[title] || 'Open project';
    if (githubLink) githubLink.textContent = 'GitHub repo';
  });
});
