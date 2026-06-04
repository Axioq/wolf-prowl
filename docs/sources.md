# Discovery Sources

Wolf Prowl starts with RSS/Atom feeds as the first discovery provider.

RSS/Atom is preferred for the first build because feeds are easy to poll, easier to test, and less brittle than scraping search results or arbitrary web pages.

## Source Rules

- Do not add a new search provider without documenting it here first.
- Keep every provider behind the discovery interface so providers can be swapped or combined later.
- Treat source content as unreliable until URLs, dates, and activity status are validated.
- Prefer feeds with clear titles, canonical links, publish dates, and summaries.
- Keep sample or placeholder feeds disabled in committed config.

## Initial Source Types

- RSS feeds for contest, giveaway, sweepstakes, and deal communities.
- Atom feeds from blogs, brand newsrooms, or hobby sites that publish promotions.
- Auction feeds from public auction, surplus, or marketplace sites when official feeds are available.

## Candidate Source Ideas

Useful places to look for RSS/Atom feeds:

- Giveaway and contest blogs that publish RSS feeds.
- Deal forums or community sites with RSS feeds for tagged searches.
- Brand or publisher blogs for topics of personal interest.
- Government surplus and public auction sites with feed support.
- Hobby-specific forums that expose RSS feeds for categories or tags.

Avoid scraping search result pages in the first version. If search APIs are added later, document the provider, cost, rate limits, API key handling, and terms of use here before implementation.

## Live Feed Testing

Use live feeds manually, not in automated tests. Automated tests should keep using fake feed data so they stay repeatable and do not depend on external sites.

For manual testing, copy the real-feed example config and enable one to three feeds at a time:

```bash
cp config/wolf-prowl.real-feeds.example.yaml config/wolf-prowl.local.yaml
```

Then edit `config/wolf-prowl.local.yaml`, set selected sources to `enabled: true`, and run:

```bash
.local/bin/uv run wolf-prowl run --config config/wolf-prowl.local.yaml
```

`config/wolf-prowl.local.yaml`, `data/`, and `digests/` are ignored by git.

Start with broad public feeds only to understand real data shape. Move generally useful source patterns into this file once they prove useful.

## Candidate Public Feed Patterns

- Reddit RSS search feeds such as `https://www.reddit.com/search.rss?q=giveaway&sort=new`.
- Reddit RSS search feeds for `sweepstakes`, `contest`, or `auction`.
- Deal/community sites that expose official RSS feeds for searches, tags, or forums.
- Public auction sites with official RSS/Atom feeds.

## Topic-Driven Search Feeds

Use `source_templates` when you want Wolf Prowl to generate RSS search feeds from topic keywords and opportunity terms.

For example, a cycling topic can define cycling terms separately from opportunity terms:

```yaml
topics:
  - name: cycling
    keywords:
      - cycling
      - bike
      - bicycle
      - mountain bike
      - gravel bike
      - road bike
    opportunity_terms:
      - giveaway
      - contest
      - sweepstakes
    excluded_terms:
      - expired
      - closed

source_templates:
  - name: Reddit search
    type: rss
    url_template: https://www.reddit.com/search.rss?q={query}&sort=new
    topics: [cycling]
    enabled: true
    max_queries_per_topic: 8
```

This generates RSS sources for combinations such as `cycling giveaway`, `cycling contest`, `bike sweepstakes`, and `mountain bike giveaway`.

Use `max_queries_per_topic` to keep broad topics from generating too many feeds.

## Example Config

```yaml
sources:
  - name: Example giveaway RSS feed
    type: rss
    url: https://example.com/giveaways.xml
    topics: [general]
    enabled: false

  - name: Example auction Atom feed
    type: atom
    url: https://example.com/auctions.atom
    topics: [general]
    enabled: false
```
