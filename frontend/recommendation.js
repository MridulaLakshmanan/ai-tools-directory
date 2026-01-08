// ===============================
// BASIC NLP HELPERS
// ===============================
const STOP_WORDS = ["for", "the", "to", "and", "of", "with", "me", "i", "want"];

function tokenize(text) {
  return text
    .toLowerCase()
    .split(/\s+/)
    .filter(word => !STOP_WORDS.includes(word));
}

// ===============================
// INTENT DETECTION
// ===============================
export function detectIntent(query) {
  const toolHints = ["alternative", "replace", "similar", "like"];
  const words = tokenize(query);

  if (toolHints.some(h => words.includes(h))) {
    return "tool";
  }
  return "category";
}

// ===============================
// CATEGORY MATCHING
// ===============================
export function matchCategories(query, categories) {
  const words = tokenize(query);

  return categories
    .map(cat => {
      const score = cat.keywords
        ? cat.keywords.filter(k => words.includes(k)).length
        : 0;
      return { ...cat, score };
    })
    .filter(cat => cat.score > 0)
    .sort((a, b) => b.score - a.score);
}

// ===============================
// TOOL RANKING
// ===============================
export function rankTools(query, tools) {
  const words = tokenize(query);

  return tools
    .map(tool => {
      let score = 0;

      words.forEach(w => {
        if (tool.tags?.includes(w)) score += 2;
        if (tool.description?.toLowerCase().includes(w)) score += 1;
      });

      // boost by quality
      score += (tool.rating || 0) * 0.3;
      score += (tool.popularity || 0) * 0.1;

      return { ...tool, score };
    })
    .filter(t => t.score > 0)
    .sort((a, b) => b.score - a.score);
}

// ===============================
// MAIN RECOMMENDER
// ===============================
export function recommend(query, tools, categories) {
  const intent = detectIntent(query);
  const matchedCategories = matchCategories(query, categories);

  let filteredTools = tools;

  if (matchedCategories.length > 0) {
    filteredTools = tools.filter(
      t => t.category === matchedCategories[0].name
    );
  }

  const rankedTools = rankTools(query, filteredTools);

  return {
    intent,
    categories: matchedCategories.slice(0, 2),
    tools: rankedTools.slice(0, 5)
  };
}
