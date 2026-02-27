export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const host = url.hostname;

    // Route game subdomain to game.html
    if (host.startsWith('game.')) {
      const gameUrl = new URL(request.url);
      gameUrl.pathname = '/game.html';
      return env.ASSETS.fetch(new Request(gameUrl.toString(), request));
    }

    // Route resume subdomain to resume.html
    if (host.startsWith('resume.')) {
      const resumeUrl = new URL(request.url);
      resumeUrl.pathname = '/resume.html';
      return env.ASSETS.fetch(new Request(resumeUrl.toString(), request));
    }

    // Default: serve as normal
    return env.ASSETS.fetch(request);
  }
};
