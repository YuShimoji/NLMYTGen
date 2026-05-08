# sports_news visual language

`sports_news` uses original broadcast-style information graphics instead of footage, screenshots, photos, or generated people.

## Core visual direction

- dark, broadcast-like background
- restrained accent colors
- strong typography
- clean grid
- scoreboard and stat hierarchy before decoration
- no cheap clipart
- no character avatars
- no fake faces
- no external icon packs
- minimal self-made SVG badges only where labels help comprehension

## Primary modules

- Opening Breaking Card
- Scoreboard Card
- Player Stat Card
- Pitch / Play Event Card
- Trend Comparison Card
- Reaction Digest Card
- Timeline Card
- Watch Point Card
- Lower Third
- Ticker

## Secondary modules

- simple SVG badges
- geometric markers
- `FAN`, `MEDIA`, `ANALYST`, `FORUM`, `OFFICIAL` labels
- small self-made status symbols

Do not make pictograms the main visual language. If a speaker or source marker is necessary, use a minimal self-made badge rather than a profile image, character icon, animal icon, or AI-generated avatar.

## Screen rules

### One screen, one claim

Each screen should carry one concise interpretive headline.

Examples:

- `低め外角のスライダーでカウントを整える`
- `前球155km/h FFから140km/h SLへ緩急`
- `この打席の鍵は外角スライダーの見極め`

### Scoreboard hierarchy

Team scores must be dominant. Inning/status must be smaller and clearly labeled.

The viewer should first read:

```text
EAGLES 3 - 4 FALCONS
```

Then read:

```text
Top 7th / 7回表
```

### Mobile readability

Side panels should prioritize major values.

Pitcher panel:

- pitcher name
- handedness
- ERA
- today's pitch count
- today's strikeouts

Batter panel:

- batter name
- handedness
- AVG
- OPS
- today's result

Move detailed stats to separate cards when needed.

### Count/status prominence

Baseball context depends on the count. Show it near the pitch event:

- B/S/O
- count before pitch
- pitch number in plate appearance
- result: Ball / Strike / In play / Foul

### Pitch event context

Pitch event cards should support:

- current pitch
- previous pitch comparison
- pitch type
- velocity
- result
- intended/actual zone when data is available
- simple trajectory or location marker

### Avoid dictionary screens

Use sequence instead of overfilling one screen:

- Screen A: live score / current event
- Screen B: pitcher card
- Screen C: batter card
- Screen D: trend/comparison card
- Screen E: reaction digest

## Motion

Do not add Ken Burns as a generic solution. If motion is described, it should be UI state transition only:

- number appears
- line highlights
- pitch marker pulses
- card slides in
- ticker updates

Motion notes are design specs only unless a supported renderer/YMM4 route exists.
