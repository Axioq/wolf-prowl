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
