# sports_news screen template notes

These notes describe the first baseball-style screen family. They are template guidance, not a renderer implementation.

## Baseball pitch event screen

Target format: 1280x720 broadcast/data UI.

Recommended layout:

- top: scoreboard strip
- left: pitcher summary panel
- right: batter summary panel or pitch history
- center: pitch zone / trajectory panel
- bottom: count/status area and concise interpretation headline

## Required semantic hierarchy

1. Matchup and score
2. Inning/status
3. Current claim/headline
4. Pitch event
5. Player context
6. Supporting detail

The inning number must not look like another score. Team scores are larger and visually dominant; inning/status is labeled and smaller.

## Card sequence for one short segment

1. `opening_breaking_card`: what happened and why viewers should care.
2. `scoreboard_card`: current score and inning context.
3. `pitch_event_card`: the pitch or play event being explained.
4. `player_stat_card`: pitcher or batter context.
5. `trend_comparison_card`: one comparison that supports the interpretation.
6. `reaction_digest_card`: sourced reaction summary.
7. `watch_point_card`: what to watch next.

## Design connection

`BaseballInfoGraphics/` currently contains a draft baseball infographic source. Use it as a visual direction reference only:

- keep the dark broadcast/data UI direction
- retain the central strike-zone strength
- correct scoreboard hierarchy
- reduce tiny side-panel text
- move dense stats into separate cards
- avoid image slots that imply third-party image use for the MVP

Do not treat `BaseballInfoGraphics/` as a production renderer or proof artifact for `sports_news`.
