document.addEventListener('DOMContentLoaded', () => {
  const profileImage = document.querySelector('.avatar-image');
  if (profileImage) {
    profileImage.src = 'data:image/jpeg;base64,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';
  }

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
    'Financial Future Dashboard': `
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
            <div class="agent-node">Agent router</div><div class="agent-arrow">→</div>
            <div class="agent-node">Tool result</div>
          </div>
        </div>
      </div>`,
    'AI Study Buddy with RAG': `
      <div class="project-preview">
        <div class="preview-label">RAG Study Assistant</div>
        <div class="preview-window">
          <div class="rag-flow">
            <div class="rag-step">Document</div>
            <div class="rag-step">Retrieve<br>context</div>
            <div class="rag-step">Grounded<br>answer</div>
          </div>
          <div class="rag-answer">Question → relevant chunks → grounded answer.</div>
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
            <div class="game-pill">Computer opponent</div>
            <div class="game-pill">Hints + commentary</div>
            <div class="game-pill">Score tracking</div>
          </div>
        </div>
      </div>`
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
    if (projectLink) projectLink.textContent = title?.includes('Games') ? 'Play demo' : 'Live demo';
    if (githubLink) githubLink.textContent = 'Source code';
  });
});
