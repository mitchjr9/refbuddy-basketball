"""
RefBuddy — Your Minnesota HS Basketball Referee Assistant
Version 1.0 — Hybrid CORE_KNOWLEDGE: 2023-2024_NFHS_Basketball_Rulebook.md baseline + 2023-2026 Changes

Adapted from RefBuddy Football v3.1 — all football references replaced with basketball.

Tabs: 🏀 Home | 🎬 Game Film | 📊 RefGrade | 👥 Assignor Hub | 📝 Quiz & Drills
Run:  streamlit run app.py
"""

# ── Standard library ──────────────────────────────────────────────────────────
import base64
import datetime
import json
import os
import subprocess
import sys
import tempfile
import urllib.parse

# ── Third-party ───────────────────────────────────────────────────────────────
import anthropic
import streamlit as st

# ── OpenCV — auto-install if missing ─────────────────────────────────────────
try:
    import cv2
    OPENCV_AVAILABLE = True
except ImportError:
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "opencv-python-headless", "-q"]
        )
        import cv2
        OPENCV_AVAILABLE = True
    except Exception:
        OPENCV_AVAILABLE = False


# =============================================================================
# CORE KNOWLEDGE BASE
# =============================================================================

CORE_KNOWLEDGE = """
# RefBuddy Core Knowledge Base
## Minnesota High School Basketball — Referee Reference

---

## 0. 2023–2026 NFHS & MSHSL RULES CHANGES & UPDATES

> **INSTRUCTION FOR ALL RESPONSES:** Default to the `2023-2024_NFHS_Basketball_Rulebook.md` baseline (Sections 1–10 below) for any question unless a specific update in THIS section overrides it. Always cite the year when a change applies. If a rule changed in 2023-24 and was further updated in 2025-26, note both years.

---

### 2023-24 Rule Changes (Baseline Season)

**[2023-24] Bonus Free Throw System Revamped — Rule 4-8-1**
- **Old:** One-and-one bonus beginning with the 7th team foul in the half; two-shot bonus on the 10th.
- **New:** NO one-and-one. Two free throws (bonus) beginning with the team's **5th foul in each quarter**. Team fouls reset to zero at the end of each quarter.
- **MSHSL EXCEPTION:** MSHSL retains the old half-based system — 1&1 on 7th team foul per half; two-shot bonus on 10th foul per half (Minnesota Modification K).
- **Why it matters:** HUGE divergence. In NFHS-only games (non-MSHSL), the quarter-reset applies. In ALL MSHSL varsity games, use the half-based 1&1/double-bonus system. Always confirm which system applies at pregame.

**[2023-24] Four Designated Throw-In Spots — Rules 4-36, 6-4-3, 7-5-2 through 4**
- **Old:** General throw-in spots with less specific guidance on frontcourt retentions.
- **New:** When a team retains or gains team control in its frontcourt (due to a violation, common foul prior to bonus, or other stoppages other than out-of-bounds), four designated spots apply: the nearest 28-foot mark on each sideline OR the nearest spot 3 feet outside the lane line on the end line.
- **Updated 2025-26:** The 3-point line now serves as the line of demarcation. Inside the arc = end-line spot (3 ft outside lane); outside the arc = 28-foot sideline spot. Uses visible court markings instead of imaginary lines.
- **Why it matters:** Determines where you hand/bounce the ball for most non-OOB stoppages in the frontcourt. Know your court markings.

**[2023-24] Like-Colored Uniform Bottoms — Rule 3-4-5**
- **New:** Teammates must all wear like-colored uniform bottoms but may wear multiple styles.
- **Why it matters:** Equipment check — all bottoms same color even if different cut/style.

**[2023-24] Undershirt Color — Visiting Team — Rule 3-5-6**
- **New:** Visiting team may wear undershirts that are black OR a single solid color similar to the jersey torso. All teammates must match.
- **Why it matters:** Common uniform question. Visitor can choose black or team color but all must wear the same.

**[2023-24] Shot Clock Operator Location — Rule 2-1-3 NOTE**
- **New:** Shot clock operator shall be seated at the scorer's and timer's table.
- **Why it matters:** Pregame — confirm operator is at the table, not elsewhere.

**[2023-24] Throw-In Correction Window — Rule 7-6-6**
- **New:** An official who administers a throw-in to the wrong team may correct the mistake before the first dead ball after the ball becomes live, unless there is a change of possession.
- **Why it matters:** You can fix a wrong throw-in team without a foul or technical — but only before first dead ball or change of possession.

**[2023-24] Stepping Out of Bounds — Rule 9-3-3**
- **New:** A player may step out of bounds without penalty unless: (a) they are the first to touch the ball after returning to court, or (b) they left the court to avoid a violation.
- **Why it matters:** Clarifies that incidental OOB stepping (e.g., player pushed OOB) is not automatically a violation. The violation triggers only if that player touches the ball first.

---

### 2024-25 Key Points & Mechanics Updates

**[2024-25] Flopping — New Warning System (MSHSL Adopted)**
- **Old:** Faking being fouled was a player technical foul.
- **New:** First team flopping = team WARNING (no technical). Second and subsequent offenses by SAME TEAM = team technical foul (2 FTs + ball at division line).
- **Mechanics:** Show flop signal (#23) during live play, note the time. If offense is advancing, let play continue; issue warning at next dead ball. Do NOT stop play if offense is moving toward basket on a defensive flop.
- **Key point:** Flopping warning doesn't require player to fall — bobbing head, flailing arms counts.
- **Why it matters:** Don't confuse with the five delay-of-game warnings. Flopping warning is a separate category.

**[2024-25] Throw-In Spot — 3-Point Line as Demarcation (Mechanics)**
- Officials use the three-point line to determine frontcourt throw-in spots.
- Inside 3-pt line → end line spot (3 ft outside lane).
- Outside 3-pt line → 28-foot sideline mark.
- Back-court stoppages → four designated spots based on ball location relative to 3-pt line (backcourt tick marks added).

**[2024-25] Uniform Number Contrast (MSHSL memo 12/20/24)**
- Numbers on dark uniforms must clearly contrast. Best practice: white numbers on dark jersey. MSHSL memo from Lisa Quednow, Phil Archer, Jason Nickleby (12/20/24).
- Do NOT stop game for uniform issues — address at next dead-clock opportunity. Repeat issues = contest report.

---

### 2025-26 Rule Changes (Current Season)

**[2025-26] No Offensive Goaltending — Rules 4-22-1 & 4-22-2 (MAJOR)**
- **Old:** Offensive goaltending was a violation.
- **New:** Offensive goaltending violations are ELIMINATED. Only defensive players can commit goaltending.
- **Why it matters:** HUGE change. If an offensive player tips/touches the ball on a downward flight that could enter the basket — NO call. No need to judge "try vs. pass" for offensive team.

**[2025-26] Ball Contacting Backboard = Downward Flight — Rule 4-22-3 (NEW)**
- **New:** Once the ball contacts the backboard, it is automatically considered to be on its downward flight. If a player then touches the ball that has contacted the backboard and has a possibility of entering the basket = GOALTENDING.
- **Why it matters:** Clarifies a common misconception. After backboard contact, always treat the ball as being in downward flight for goaltending purposes.

**[2025-26] Basket Interference — Backboard Slap — Rules 4-6-1a & 4-6-1b (NEW)**
- **New:** Basket interference NOW INCLUDES: a player slapping or striking the backboard, causing it to vibrate, while the ball is on/within the basket, touching the backboard, or within the cylinder.
- **Why it matters:** Formerly just a technical foul. Now it's ALSO basket interference — the points count if the ball would have gone in.
- **Situation:** B1 slaps backboard → basket vibrates while ball is in basket → TWO violations: (1) basket interference = 2 pts awarded, (2) technical foul = 2 FTs + ball at division line. Both are penalized.

**[2025-26] Player Definition Updated — Rule 4-34-1**
- **New:** A player is one of the five team members legally on the court at any time, EXCEPT during time-outs or intermissions.
- **Why it matters:** During a timeout, all players are bench personnel. Technical fouls on bench personnel during timeouts = indirect tech to head coach (loss of coaching box privileges).

**[2025-26] Throw-In Spot — 3-Point Line Demarcation — Rule 7-5-4**
- **New:** The three-point line (visible court marking) now determines the designated throw-in spot following a stoppage in the frontcourt (not due to OOB). Inside = end line. Outside = 28-foot line.
- **Why it matters:** Uses visible markings; eliminates the imaginary line confusion from the prior system.

**[2025-26] Thrower Delay OOB — Now a Violation — Rules 9-2-12 & 9-3-4 (NEW)**
- **Old:** Thrower who stepped out of bounds to deceive and then touched ball = technical foul.
- **New:** This is now a VIOLATION (turnover), not a technical foul.
- **Why it matters:** Lesser penalty, easier to enforce consistently. Player cannot step out of bounds as a thrower to deceive and be first to touch the ball back in bounds.

**[2025-26] Backboard Contact Technical — Rule 10-4-4b**
- **New:** Players may not illegally contact the backboard or ring in ways that create unfair advantage or interfere with a scoring attempt. Technical foul.
- **Why it matters:** Closes gap between basket interference and technical fouls; removes subjective intent standard.

**2025-26 Points of Emphasis:**
1. **Contact on the Ball Handler** — Hand-checking, body displacement (hips/torso), and impeding freedom of movement are fouls. NOT all late-game fouls are intentional. Determine by the ACT, not the coach's verbal instructions ("foul," "red," "scramble"). Consistent standards throughout entire game.
2. **Bench Decorum, Communication, and Player Altercations** — Apply Rule 4-48 (Warning for Coach/Team Conduct) early. Acknowledge reasonable coach inquiries (nod is sufficient). Rules-based questions deserve a clear informative response.
3. **Faking Being Fouled (Flopping)** — First offense: team warning. Subsequent offense: team technical. Don't stop advancing play on a defensive flop.

---

### Quick-Reference: Rules That CHANGED from 2023-24 Baseline

| Rule | Year | What Changed |
|------|------|-------------|
| 4-8-1 | 2023-24 | Bonus = 5th team foul/quarter (2 FTs); no 1&1 [NFHS only — MSHSL retains 1&1 half system] |
| 4-36, 7-5-2–4 | 2023-24 | Four designated frontcourt throw-in spots established |
| 3-4-5 | 2023-24 | Like-colored uniform bottoms required |
| 3-5-6 | 2023-24 | Visiting undershirt: black or jersey color (team must match) |
| 7-6-6 | 2023-24 | Wrong throw-in team correctable before first dead ball / change of possession |
| 9-3-3 | 2023-24 | Stepping OOB not a violation unless first to touch ball on return |
| 2-1-3 NOTE | 2023-24 | Shot clock operator must sit at scorer's/timer's table |
| Flopping rule | 2024-25 | Player tech → team warning (1st); team tech (2nd+) |
| 7-5-4 | 2024-25 / 2025-26 | 3-pt line as demarcation for frontcourt throw-in spot |
| 4-22-1 & 2 | 2025-26 | Offensive goaltending ELIMINATED |
| 4-22-3 | 2025-26 | Ball touching backboard = automatically on downward flight |
| 4-6-1a/b | 2025-26 | Backboard slap causing vibration = basket interference |
| 4-34-1 | 2025-26 | Players become bench personnel during time-outs |
| 9-2-12, 9-3-4 | 2025-26 | Thrower delay OOB = violation (was technical foul) |
| 10-4-4b | 2025-26 | Backboard/ring contact creating unfair advantage = technical foul |

---

---

## 1. NFHS RULE HIERARCHY & KEY CITATIONS

### Rule 1 — The Court and Equipment
- **Court:** 84' × 50' recommended (max 94' × 50'). Division line bisects court (Rule 1-3).
- **Basket height:** 10 feet above floor; ring 18" inside diameter; net 15–18" long (Rule 1-10, 1-11).
- **Ball — Boys:** 29.5–30" circumference, 20–22 oz (Rule 1-12).
- **Ball — Girls:** 28.5–29" circumference, 18–20 oz (Rule 1-12).
- **NFHS Authenticating Mark** required on game balls (Rule 1-12-1g).
- **Backboard padding required** on bottom/sides up to 15" from bottom (Rule 1-9).
- **Coaching box:** 28-foot maximum, state option (Rule 1-13-2). **MSHSL: 14 feet** (MN Mod I).
- **Officials arrive:** Minimum 15 minutes before scheduled start (Rule 2-2-2).
- **Officials' uniform:** Black-and-white striped shirt, black pants, predominantly black shoes/socks (Rule 2-1-1). **MSHSL: Smitty gray shirt with black panel, MSHSL logo on left crest** (MN Mod J).

### Rule 2 — Officials and Their Duties
- **Referee's pregame:** Inspect/approve equipment, designate timepiece, official scorebook, notify teams 3 min before each half, verify coaches confirm legal uniforms (Rule 2-4).
- **No replay equipment** — officials may not use video/replay to make decisions during game (Rule 2-2-1). EXCEPTION: State championship series may permit replay for last-second shot at 0:00.
- **Referee has final authority** on any matter not specifically covered in rules (Rule 2-3).
- **3-person crew:** Referee (R), Umpire 1 (U1/Trail), Umpire 2 (U2/Center or Lead).
  - Lead (L) = under basket official; Trail (T) = half-court; Center (C) = middle position.

### Rule 3 — Uniforms and Equipment
- **Jersey numbers:** Must be 0–5, 10–15, 20–25, 30–35, 40–45, 50–55 (numerals that can be indicated with one hand). No duplicates within a team (Rule 3-4-3).
- **Jersey colors:** Home = white; Visitor = dark (Rule 3-4-1). **MSHSL Mod B:** Home = dark; Visitor = white (opposite of NFHS!).
- **Number contrast (MSHSL memo 12/20/24):** Numbers on dark uniforms must clearly contrast. Best practice = white numbers.
- **Undershirts (home):** Must be white, hemmed (Rule 3-5-1). **Undershirts (visitor):** Single solid color similar to jersey torso OR black; all teammates must match (Rule 3-5-6 [2023-24 change]).
- **Compression apparel:** Black, white, beige, or predominant jersey color; all teammates same color. **MSHSL Mod C:** All apparel (wristbands, headbands, sleeves, knee pads, compression) must be solid black OR white; same color for all participants.
- **Jewelry prohibited** (Rule 3-5-3). Medical alert jewelry may be taped.
- **Headbands/wristbands:** Single solid color, must match teammates (Rule 3-5-3c). MSHSL: must be black or white.

### Rule 4 — Definitions
- **Backcourt/Frontcourt:** Team's frontcourt = between its end line and nearer edge of division line, including its basket (Rule 4-13).
- **Bonus:** 2 FTs awarded for common foul beginning with 5th team foul per quarter (NFHS Rule 4-8-1). **MSHSL: 1&1 on 7th foul per half; double bonus on 10th** (MN Mod K).
- **Closely Guarded:** Opponent within 6 feet in player's frontcourt, holding or dribbling the ball. 5-second count applies (Rule 4-10). **MSHSL EXCEPTION (Mod F):** Closely guarded is NOT in effect when player is DRIBBLING the ball (only applies to player holding the ball).
- **Control (Player):** Holding or dribbling a live ball (Rule 4-12-1).
- **Control (Team):** While player controls, live ball passed among teammates, interrupted dribble, or player has disposal for throw-in (Rule 4-12-2).
- **Dribble:** Begins when player pushes/throws/bats ball to floor before pivot foot is lifted; ends when ball rests in hand(s), both hands touch simultaneously, or ball becomes dead (Rule 4-15).
- **Foul types:** Common foul (Rule 4-19-2), intentional foul (Rule 4-19-3), flagrant foul (Rule 4-19-4), technical foul (Rule 4-19-5), player-control foul (Rule 4-19-6), team-control foul (Rule 4-19-7).
- **Goaltending [2025-26 UPDATED]:** (a) Defensive player touches ball during try/tap while ball is in downward flight entirely above ring level with possibility of entering basket, not touching cylinder (Rule 4-22-1). (b) Ball contacting backboard = automatically on downward flight (Rule 4-22-3 NEW). NO more offensive goaltending (Rule 4-22-1 & 2 [2025-26]).
- **Guarding (legal):** Both feet on floor, torso facing opponent. Max 6 feet in closely guarded (Rule 4-23).
- **Held ball:** Opponents' hands firmly on ball so control can't be obtained without undue roughness (Rule 4-25).
- **Pivot:** Stepping with same foot while other (pivot) foot kept at point of contact (Rule 4-33).
- **Player [2025-26 UPDATED]:** One of five team members legally on court; becomes bench personnel during time-outs and intermissions (Rule 4-34-1).
- **Secondary Defender (MSHSL restricted area):** Teammate who helped a primary defender beaten by offensive player (head/shoulders past defender); or double-teams low post; or is outnumbered in fast break (MSHSL addendum Rule 4-41).
- **Restricted Area (MSHSL addendum Rule 4-38):** 4-foot radius arc from center of basket to inside of arc line, extending to face of backboard. Secondary defender "in" area when any part of either foot is in or above this area.
- **Traveling:** Moving pivot foot or taking more than allowed steps while holding ball (Rule 4-44 / 9-4-1).

### Rule 5 — Scoring and Timing
- **Goal:** Ball enters basket from above and remains/passes through net; counts for team into whose basket it falls regardless of who threw it (Rule 5-1).
- **Field goal value:** 2 points; 3 points if from beyond 3-point line (Rule 5-1-2,3).
- **Free throw:** 1 point (Rule 5-1-4).
- **Game length:** Four 8-minute quarters (Rule 5-4). **MSHSL Mod A:** Two 18-minute halves (varsity); max 16-minute halves below varsity.
- **Extra period:** 4 minutes for overtime (Rule 5-7).
- **Game clock stops:** On every foul, violation, held ball, OOB, time-out, etc. (Rule 5-8).
- **Time-outs:** 3 full (60-second) time-outs per team regulation + 1 per OT period; 1 additional for second OT and beyond; unlimited 30-second time-outs (Rule 5-11).
- **Mercy Rule (MSHSL Mod G):** When point differential reaches **35 or more** with **less than 9 minutes remaining** in second half → running clock. Clock stops only for time-outs. Shot clock continues. Returns to regular timing if differential drops to **less than 30**.

### Rule 6 — Live Ball/Dead Ball
- **Ball becomes live:** On a throw-in, when the ball is released; on a jump ball, when the ball leaves the official's hand; on a free throw, when at the disposal of the free thrower (Rule 6-1).
- **Ball becomes dead:** On any foul, violation, held ball, time-out, successful goal, when period expires (Rule 6-7).
- **Resumption-of-play procedure:** After certain violations — no substitute, no time-out, no delay (Rule 4-38).

### Rule 7 — Out of Bounds and the Throw-In
- **Out of bounds:** When ball or player touches the boundary line, floor, or objects on/outside it (Rule 7-1).
- **Responsibility:** Last player to touch ball before it goes OOB is responsible (Rule 7-2).
- **Throw-in administration (TRAIL):** Bounce pass or direct pass; 5-second count; thrower may not leave spot until ball is released (Rule 7-6).
- **Four designated throw-in spots (frontcourt, 2025-26 updated Rule 7-5-4):**
  - **Inside 3-pt line** (stoppage occurred inside 3-pt line or on 3-pt line) → end line, 3 feet outside lane line (nearest to stoppage).
  - **Outside 3-pt line** (stoppage occurred outside arc) → 28-foot sideline mark nearest to stoppage.
  - These apply when team retains/gains possession in frontcourt due to violation, common foul (pre-bonus), or stoppages other than OOB.
- **Throw-in violations (Rule 7-6-7):** Leaves spot, 5-second count, passes through basket without touching player, steps on/over boundary before released, etc.
- **Thrower delay OOB [2025-26 NEW Rule 9-2-12 & 9-3-4]:** Purposely stepping OOB as thrower then being first to touch ball in bounds = VIOLATION (was technical foul).
- **Wrong team throw-in correction (Rule 7-6-6):** Can correct before first dead ball / change of possession.

### Rule 8 — Free Throw
- **Free thrower:** In semicircle, behind free-throw line. 10-second limit after ball at disposal (Rule 8-3).
- **Free thrower violations (Rule 9-1):** Cross line before ball touches ring/board/basket = ball dead on violation; opponent's violation = ball live (attempt counts if successful) or retake.
- **Lane occupancy:** Players take assigned lane spaces; alternating positions within 3 feet of lane; may not enter until ball is released by shooter (Rule 8-1, 8-2).
- **Penalty:** Free throw violation by shooter = ball dead, no point; free throw violation by non-shooter on defense = if made it counts, if missed try again (Rule 9-1 penalties).
- **Technical foul free throws:** 2 FTs, no lane players, ball inbounded at division line opposite scorer's table after last FT.

### Rule 9 — Violations and Penalties
- **Throw-in violations (Rule 9-2):** 5-second count, leave designated spot, enter court before released, thrower-in contacted (PENALTY: intentional foul on contact with thrower-in), ball passed through basket directly.
- **Out of bounds (Rule 9-3):** Ball awarded to opponents. Player may step OOB without penalty unless first to touch ball on return or left court to avoid violation (Rule 9-3-3).
- **Traveling (Rule 9-4):** Pivot foot lifted and replaced, two steps without dribble, jumping with ball and not releasing before touching floor.
- **Illegal dribble (Rule 9-5):** Dribble with two hands, carry/palm, dribble a second time after dribble ends (double dribble).
- **Three seconds (Rule 9-7):** Player in their team's frontcourt may not remain in the lane for more than 3 consecutive seconds while team is in control and clock is running.
- **Ten seconds (backcourt) (Rule 9-8):** Team must advance from backcourt to frontcourt within 10 seconds. **MSHSL:** Use shot clock for 10-second count when shot clock is operating.
- **Backcourt violation (Rule 9-9):** Once ball established in frontcourt, team in control may not return to backcourt. Note: if offense last touches in frontcourt and first touches in backcourt = violation.
- **Closely guarded (Rule 9-10):** Holding ball in own frontcourt while closely guarded for 5 consecutive seconds = violation. **MSHSL Mod F:** NOT in effect while DRIBBLING.
- **Goaltending/Basket interference (Rule 9-11 / 4-6, 4-22 [2025-26]):**
  - Goaltending: defensive player touches ball on downward flight above ring level (or after backboard contact per new Rule 4-22-3) = 2 pts awarded.
  - Basket interference: touching ball/basket while ball is in/on basket, or within cylinder; also backboard slap causing vibration while ball in/on basket (Rule 4-6-1a/b NEW 2025-26) = 2 pts awarded.
  - Offensive goaltending ELIMINATED (2025-26).
- **Kicking/fisting ball (Rule 9-4-3):** Intentional striking = violation (ball to opponents).
- **Excessive swinging of arms/elbows (Rule 9-12):** Violation if it endangers opponent.

### Rule 10 — Fouls and Penalties
- **Administrative technical foul (Rule 10-1):** Roster errors, equipment violations, delay.
- **Team technical foul (Rule 10-2):** Delay of game after warning, too many players, improperly worn equipment after warning.
- **Player technical foul (Rule 10-4):** Unsporting act, delay, illegal equipment, taunting, hanging on rim, backboard slap (Rule 10-4-4b [2025-26]).
- **Bench technical foul (Rule 10-5):** Coach, substitute, team attendant, or follower commits unsporting acts. Bench tech = indirect tech to head coach = loss of coaching box.
- **Head Coach's Rule (Rule 10-6):**
  - Direct tech: assessed directly to head coach for abusive conduct. Coach gets 2 FTs against them; flagrant or second direct = ejection.
  - Indirect tech: bench tech charged to bench member → indirect tech charged to head coach. First indirect = warning, loss of coaching box. Second indirect in same half = ejection of head coach.
- **Personal foul penalty:** Offended player shoots FTs (if in bonus), or throw-in if not in bonus.
- **Intentional foul penalty:** 2 FTs + throw-in at point of interruption regardless of bonus.
- **Flagrant foul:** 2 FTs + throw-in; offender ejected (Rule 10-7-12).
- **Player disqualification:** 5th foul (personal + technical fouls combined); 2 tech fouls; 1 flagrant foul (Rule 4-14).
- **Technical foul penalty:** 2 FTs; ball at division line opposite scorer's table. Counts as team foul.

---

## 2. MSHSL MINNESOTA-SPECIFIC RULES & MODIFICATIONS

### Key Minnesota Modifications (December 2025)
- **Mod A — Game Length (Varsity):** Two 18-minute halves (not quarters). JV/sub-varsity: max 16-minute halves.
- **Mod B — Uniform Colors:** HOME = dark uniforms; VISITOR = white uniforms. (OPPOSITE of NFHS default.)
- **Mod C — Apparel Colors:** All apparel (excluding knee braces) — wristbands, headbands, arm/knee sleeves, knee pads, compression shorts, tights — must be solid **black or white**, same color for all participants.
- **Mod D — Sub-Varsity:** Also played in halves, max 16 minutes.
- **Mod E — Shot Clock:** 35-second shot clock mandatory for ALL varsity games, including extra periods. (Adopted 2023-24.)
- **Mod F — Closely Guarded Exception:** Closely guarded rule (5-second count) is NOT in effect when player is dribbling the ball (Rule 9-10-1a NOTE). Applies only to player holding the ball.
- **Mod G — Mercy Rule:** Point differential **35+** with **<9 minutes remaining** in the second half → running clock (game clock only stops for time-outs). Returns to regular timing if differential drops to **<30 points**. Shot clock continues throughout.
- **Mod H — Restricted Area Arc:** Required for all levels of MSHSL play. 4-foot radius from center of basket.
- **Mod I — Coaching Box:** 14 feet (NFHS maximum is 28 feet).
- **Mod J — Officials Uniform:** Smitty gray shirt with black panel, black collar, sleeve cuffs, MSHSL logo on left crest. All crew members must match.
- **Mod K — Bonus Free Throws:** 1&1 on 7th team foul per HALF; double bonus (2 FTs) on 10th team foul per half. (MSHSL does NOT use the NFHS quarter-reset system.)

---

## 3. MSHSL SHOT CLOCK — COMPLETE RULES (2025-26)

### Basics
- **Shot clock period:** 35 seconds (standard); 20 seconds (offensive rebound situations).
- **Mandatory:** All varsity games including extra periods; mercy rule games.
- **Turn off:** When game clock ≤ shot clock period (i.e., game clock ≤ 35 seconds).
- **Operator:** Seated at scorer's/timer's table. Separate distinct horn. Must have backup stopwatch and air horn.
- **Both clocks must work** to start game. If one fails → turn off both, use alternate procedure.
- **Shot clock horns do NOT stop play.** Only a whistle indicating a violation stops play.
- **Recall function:** Not required but strongly recommended.

### When Shot Clock STARTS
- Any throw-in when ball is legally touched/touches any player on court (does not need to be in possession).
- Jump ball: when ball is POSSESSED (not when it's tipped).
- Change in team control.

### RESET to 35 Seconds (Full Reset)
1. Scored basket (starts when ball legally touched after throw-in).
2. Change in team control while ball remains live.
3. Single personal foul in the BACKCOURT.
4. Kicked or fisted ball by defense in the BACKCOURT.
5. Free throw situation: set to :35 immediately; offense rebounds → reset to :20.
6. Defense causes held ball during team control; AP arrow favors defense.

### RESET to 20 Seconds (Offensive Rebound Situations)
1. Offense gains control anywhere after unsuccessful field goal that contacts ring/flange.
2. Offense gains control anywhere after unsuccessful free throw remaining in play.
3. Defense fouls after FG miss (hits rim) or during successful try, offense inbounds in frontcourt.
4. Defense causes ball OOB after FG/FT miss (hits rim), offense retains possession in frontcourt.
5. AP arrow favors offense after held ball following shot that hit rim (prior to team control).
6. Offensive foul in their BACKCOURT; defense awarded ball in their frontcourt.
7. Held ball; defense awarded ball in their frontcourt.
8. Violation; defense awarded ball in their frontcourt.
9. Double personal foul, one intentional/flagrant on offense; defense awarded ball in frontcourt.
10. Shot hits rim/flange, batted into backcourt OOB by offense; defense gets ball in their frontcourt.

### RESET to 20 Seconds OR TIME REMAINING (whichever is greater)
1. Personal foul by defense, ball inbounded in frontcourt by offense (shot clock was above 20).
2. Kicked/fisted ball by defense, ball inbounded in frontcourt by offense.
3. Inadvertent whistle, no player/team possession, AP arrow favors either team in frontcourt.

### NO RESET (Unexpired Time Remains)
- Ball deflected OOB retained by offense (offense threw it OOB during a pass — stays same).
- Time-out.
- Double foul.
- Defense causes held ball during team control; AP arrow favors OFFENSE → NO reset.
- Defense commits foul/violation → frontcourt throw-in by offense, shot clock above :20 → NO reset (leave it above 20; only reset if at/below 20).

### Shot Clock Violation
- Signal: Two hands above head, index fingers extended; verbal "shot clock."
- Shot clock horn doesn't stop play — official must whistle.

### Officials Signals to Table
- Shot clock violation: two hands overhead with index fingers extended.
- Reset to 35: circle/roll hands signal (full reset).
- Reset to 20: one arm extended at 90-degree angle.

---

## 4. MECHANICS — 3-PERSON CREW POSITIONING (MSHSL)

### General Positioning
- **Lead (L):** Under the basket, baseline side opposite ball. Responsible for: end line, underneath basket, block/charge calls near basket, restricted area, post play, goaltending. Works deep — at or near the end line. Mirror ball as Lead.
- **Trail (T):** Half-court side, near 28-foot mark. Primary for: 3-point attempts (signal), perimeter fouls, out-of-bounds on sideline, bounce-pass throw-in administration.
- **Center (C):** Middle of court, opposite table. Coverage: ⅓ of court, ½ of paint area. Handles: off-ball activity, top of key, secondary coverage, post area.
- **Areas of coverage:** L = ½ lane to 3-pt line; T = above lane extended to 3-pt, end line, ⅔ behind arc; C = ⅓ court, ½ of paint.

### Key Positioning Principles
- **Lead rotation (L):** Rotate when ball crosses midline of paint and drive/post threat is imminent. If rotate late and ball goes other way (shot/turnover), rotate back. If ball reversed to far corner, Lead can rotate. When 2 posts on opposite side of floor, flex/rotate.
- **Trail (T):** Has the sideline; do not get too low. Do not get straight-lined on fast break — stop at FT line. Call out of primary only by coming in strong under the 3-pt line.
- **Center (C):** Has other sideline from Trail. Back on press defense. Count down from 5 visible at end of half. Be deliberate but not robotic.
- **Stick around huddle until 2nd horn for timeout** — get teams out on time.
- **As Lead:** If ball crosses midline of paint and drive/post threat imminent → rotate. After rotation, if ball goes away → rotate back.

### Pre-Game
- Arrive on court 15 minutes before tip.
- Space out across from table in typical pre-game positioning.
- Referee leads pregame conference with head coaches and captains; then meet with table.
- U1 meets with shot clock operator (standard protocol — review all 12 shot clock items).
- U2 observes both teams while U1 is at the table.
- Bounce pass on all throw-ins. Trail handles throw-in administration.
- Review: throw-in spots, shot clock resets, mercy rule, restricted area arc, flopping protocol.

### Free Throw Administration (3-Person)
- **Center (C):** Responsible for lane activity across AND shooter; administer at top of restricted arc; show visible count of shots; chop ball in; visible 10-second clock.
- **Lead (L):** Responsible for lane activity across; mirror ball.
- **Trail (T):** Assists with all activity; watches activity behind 3-pt line; only say "3/2/1" on last 3 FTs.
- When administering FT: do it at top of restricted arc; be loud and clear.

### Free Throw Protocols
- If FT count announced wrong, blow whistle and correct before ball becomes live.
- If free thrower loses ball while at disposal → violation.
- Visible 10-second backcourt count when shot clock is off; use shot clock when it's operating.

### Signaling & Communication
- **Full timeout:** Open hands (NOTE: fists = double foul — do NOT use fists for timeout).
- **Chop with hand closest to scorer's table** when inbounding ball (toward clock keeper).
- **Hit foul (contact foul):** Straight left arm (from reporter's view).
- **3-point attempt:** Hand up high; also for chopping, corrections, etc.
- **When at table:** Slow down; same foul call at spot and table; hands high when signaling numbers.
- **On a foul, go to table:** Show signal mirroring the play (signals that replicate play).
- Do NOT point out-of-bounds — use hand (palm toward table/floor).
- Correct your own calls (out-of-bounds reversals, etc.).
- Tick marks on floor: use for fouls in backcourt or violations in frontcourt.
- Midcourt inbound after technical foul (ball at division line opposite scorer's table).

---

## 5. RESTRICTED AREA ARC — MSHSL ADDENDUM

### Rule (MSHSL Addendum Rules 4-38, 4-41, 4-23-3)
- **Secondary defender CANNOT** establish initial legal guarding position IN the restricted area for the purpose of drawing a player-control foul/charge when defending a player with the ball (dribbling or shooting) or who has released ball for pass or try.
- If illegal contact occurs within restricted area → **BLOCKING FOUL** (except flagrant).
- **Exception 1:** Offensive player leads with foot/unnatural knee, or wards off with arm → **PLAYER-CONTROL FOUL**.
- **Exception 2:** Player in control stops continuous movement toward basket, then initiates contact with secondary defender in restricted area → **PLAYER-CONTROL FOUL**.
- **Exception 3 (Verticality):** Secondary defender in restricted area who jumps straight up with arms raised in legal vertical plane AND attempts to block a shot → VERTICALITY APPLIES. Does not apply if defender remains grounded.
- **Secondary defender definition:** (a) Teammate who helped primary defender beaten by offensive player (head/shoulders past); (b) double-teams low post player; (c) outnumbered fast-break defender (initially secondary, but may establish legal position and stay with player into arc).
- **Important:** Restricted area arc rules apply to PASS AND CRASH situations too. A secondary defender grounded in the arc trying to take a charge = blocking foul.

### Signaling Sequence for Restricted Area Block
- Option 1: Fist in air → signal block → point to restricted area (on floor below basket).
- Option 2: Fist in air → point to restricted area → signal block.
- **NOTE:** If foul is a blocking foul NOT involving the restricted area, do NOT point to the arc when signaling. That signals to partners that restricted area was a factor.
- Lead is PRIMARY on block/charge plays involving secondary defender. T and C are secondary.
- If non-calling official can provide definitive help → calling official may switch the call.

---

## 6. FLOPPING — MSHSL MECHANICS (2024-25 Adopted, Continued 2025-26)

### Rules
- **First flopping offense (by either team):** Team WARNING. Recorded in book; reported to head coach.
- **Second and subsequent offenses (same team):** TEAM TECHNICAL FOUL (2 FTs + ball at division line opposite scorer's table).
- Flopping does NOT require player to fall to floor. Includes: head bob, arm flail, dramatic reaction without contact.
- Flopping warning is NOT a violation that causes a turnover (ball does not automatically change possession on warning).
- Do NOT confuse with the five delay-of-game situations.

### Stopping Play Mechanics
- **Signal:** Show flop signal (#23/mechanic) during live play; note the time.
- **Defensive flop, offense advancing:** Do NOT stop play. Note time; issue warning at next dead ball/change of possession/when offense stops advancing.
- **Defensive flop, second offense (tech):** Stop game immediately. If shot is in air → wait for attempt to complete → penalize. Count basket if made.
- **Offensive flop, shot is in air:** Wait for rebound before issuing warning. Continuation applies.
- **Key:** Team control is lost on a shot attempt — wait for play sequence before blowing whistle.
- If warning is first offense and you stop play immediately → determine possession via AP arrow for throw-in.
- **Inbound spot for flop warning:** Tick mark where ball last was (unless shot or pass was in the air).

---

## 7. PERSONAL GAME NOTES (Selected — 2023-26 Seasons)

### 2025-26 Season

**2/13/26:** Stick around huddle until 2nd horn on timeout — ensure teams get out on time. Lead: if rotate late and ball goes away, rotate back. Pregame: start with coaches+captains, then dismiss captains for coaches-only portion.

**2/17/26:** When inbounding ball, chop with hand closest to scorer's table (clock keeper side).

**1/21/26:** Be deliberate but not robotic at the spot — use voice to explain calls/FTs/inbound spot. As Lead: if ball crosses midline of paint and drive/post threat imminent → rotate. Do NOT punch rebound foul as offensive foul — call as loose ball foul.

**12/19/25:** When running down court as new Lead, turn head and look back. Full timeout = open hands (fists = double foul). First delay of game = warning; second = technical. Example: spilling water on sideline. If other 2 officials gather, don't go over — need to watch players. Toss jump ball higher with 1 hand and more accurately.

**12/10/25:** If official administering FTs gets FT count wrong → blow whistle and correct before ball becomes live.

**West Lutheran JV/V 12/4/25:** Point at arc if restricted area blocking foul. Center: on sideline with players/not much room, move to side for better angle. Do not get too low as Trail.

**Eastview tournament 11/8/25:** Delay of game warnings, screen verbiage, contact, bench decorum, technical vs. intentional foul, post contact.

### 2024-25 Season

**If player trips on other player lying on floor = blocking foul.** Player on floor not in legal guarding position.

**Falling to ground while dribbling is NOT a travel.** Rolling on ground with ball (belly-to-back) IS a travel. Holding ball and going to ground IS travel. Dribbling and going to ground is NOT travel.

**Illegal screen:** Screener pushes defender with two hands, extends legs outside shoulder width, or extends arms making contact = team control foul.

**West Lutheran V Girls 12/17/24:** Cutting player off and reaching across body = foul. Spin dribble then 2 steps = travel. Flex/rotate as Lead when 2 posts on opposite side of floor.

**Mound Westonka 9A Boys 12/12/24:** Change hands for 5-second count to signify new count.

**Minnetonka 10A/9A Girls 12/11/24:** Only say 3/2/1 on FTs (last 3). Hit foul (contact foul) = straight left arm. Mirror ball as Lead. Number of FTs → signal toward division line when reporting. Areas: L=½ lane to 3pt; T=semicircle above lane, 3pt to endline, ⅔ behind arc; C=⅓ court, ½ paint.

**Rogers JV Girls 1/7/25:** If C: count basket and wave off game on last-second shot (if made). 1&1 handshake: don't shake — firm. Wave off shot if foul on floor.

**Secondary defender must be completely outside restricted arc on block/charge.** Pause after administering throw-in — count doesn't start right away.

**Grounded in lane = restricted area blocking foul. If jump vertically = legal.**

**If team control in frontcourt, even if tipped by other team, if offense last to touch in frontcourt and first to touch in backcourt = violation.**

**Visitation Girls V 1/23/25:** Ball reversed to far corner — Lead can rotate. Close to 10 seconds but ball pressured/trail has competitive matchup — Center needs to help.

**Edina Girls 10A/JV 1/24/25:** Call hook foul, not hold (if it's a hook).

**EP JV G 12/6/24:** Pushing player in back on layup = intentional foul.

**Fridley Girls V 1/28/25:** Remember jersey number if you call foul then tech on same player.

**Tournament 2/8/25:** Sweeping signal = player was passing. If player is pushed/swept, can use chucking signal (2 fists together, push). "Walk into" is the call — be very specific when choosing this (similarity to "walled up," coaches will question).

### Clinic Notes 2024-25

**C on 3-person FTs:** Show visible count of shots, 10-second clock, chop ball in, responsible for lane activity across AND shooter. Lead responsible for lane activity across. Trail assists all and watches behind 3-pt line.

**Tip by defender on inbounds pass is NOT a try for goal.**

**Any thrown ball from behind 3-pt arc is a 3-pt attempt** (unless deflected by offense).

**"No shot" not "on the floor" — wave off.**

**Tick marks at foul in backcourt or violation in frontcourt.**

**C back on press defense.**

**Say "no shot" when waving off.**

### Preseason/Clinic 2025-26

**Throw-in spots:** 3-pt arc instead of trapezoid — Outside (arc) = 28 ft; Inside (arc) = baseline.

**No offensive goaltending (basket interference) — 2025-26 change.**

**Slapping backboard/ring = technical foul (and basket interference if ball is in/on basket).**

**Points of emphasis:** Bench decorum and communication (pregame: only talk to head coach; warnings then techs); contact with ball handler (blow whistle early and set parameters; freedom of movement; low post contact).

---

## 8. COMMON REFEREE PITFALLS & CORRECT CALLS

1. **Fists for timeout signal** → WRONG. Open hands = full timeout. Fists = double foul.
2. **Stopping play on defensive flop while offense advancing** → WRONG. Note time; issue at dead ball.
3. **Calling offensive goaltending (2025-26)** → WRONG. Eliminated. Only defensive goaltending exists.
4. **Not pointing to restricted area when signaling restricted area block** → Missed mechanic. Signal sequence is critical.
5. **Secondary defender in restricted area jumping vertically → calling it a block** → WRONG if they jumped straight up within vertical plane attempting to block shot. Verticality applies.
6. **Treating closely guarded as applying to dribbler (MSHSL)** → WRONG. MN Mod F: 5-second closely guarded count does NOT apply while player is dribbling.
7. **Using NFHS quarter-based bonus in MSHSL games** → WRONG. MSHSL retains 1&1 on 7th team foul per HALF; double bonus on 10th.
8. **Forgetting home team wears dark in Minnesota** → WRONG vs. NFHS default. MSHSL Mod B: home = dark.
9. **Not resetting shot clock to 20 on offensive rebound that contacts rim** → WRONG. Any shot that hits rim/flange = hold button, wait for possession, then reset (off. = 20, def. = 35).
10. **Starting shot clock count immediately on jump ball** → WRONG. Shot clock starts when ball is POSSESSED on a jump ball, not when tipped.
11. **Giving throw-in to wrong team and not correcting** → Can be corrected before first dead ball / change of possession (Rule 7-6-6).
12. **Not using 3-pt line for throw-in spot (2025-26)** → Use visible 3-pt line. Inside = end line spot; outside = 28-foot mark.
13. **Calling flopping as a player technical** → WRONG since 2024-25. First offense = team WARNING; second = team technical.
14. **Home team wearing white uniforms in MSHSL** → Uniform violation. Home = dark; visitor = white (Mod B).
15. **Not having U1 pregame the shot clock operator** → Mandatory every game since 2024-25 season.

---

## 9. FRONT COURT / BACK COURT — KEY SITUATIONS

- If team in control in frontcourt: even if ball is tipped by defender, if offense is last to touch in frontcourt AND first to touch in backcourt → BACKCOURT VIOLATION.
- Ball passed from frontcourt, touches backcourt before player touches it: player who touches it in backcourt — if from the same team (offense), backcourt violation.
- Division line is part of the backcourt (Rule 4-13-2).
- Defensive player may take ball into backcourt. Backcourt violation only applies to the team that last had team control in the frontcourt.

---

## SYSTEM PROMPT INSTRUCTIONS FOR REFBUDDY

You are RefBuddy, a hyper-precise Minnesota high school basketball referee assistant.

CRITICAL LAYERING RULE: The CORE_KNOWLEDGE contains a `2023-2024_NFHS_Basketball_Rulebook.md` baseline (Sections 1–9) plus 2023-2026 changes (Section 0) at the top.
- DEFAULT to the `2023-2024_NFHS_Basketball_Rulebook.md` for any rule not listed in Section 0.
- If Section 0 contains a change for that rule, APPLY the updated rule and cite the year: e.g., "[2025-26 change]" or "[2025-26 change — overrides 2023-24 Rule X-X-X]".
- MSHSL Minnesota Modifications ALWAYS take precedence over NFHS rules for MSHSL games.
- Never cite NFHS language when MSHSL has a conflicting modification.

Your behavior:
1. Start EVERY response with the most relevant rule citation (e.g., "Rule 4-22-1 [2025-26 change]" or "MSHSL Mod G") and include the year if the rule changed.
2. Reference personal game notes when applicable.
3. End EVERY response with: "*Not official MSHSL interpretation — confirm with your assignor.*"
4. Temperature = 0 mindset: maximum precision, no guessing, no hallucinating.
5. If game context (quarter vs. half, crew size, level, MSHSL vs. NFHS) is missing, ask before ruling.
6. For video/film analysis: always include a VISIBILITY CHECK section. Use "Frame N" format.
7. For RefGrade evaluations: structured scores (0-100), frame-by-frame highlights, visibility notes, "What to work on" bullets.
8. MSHSL CRITICAL DIFFERENCES TO ALWAYS REMEMBER:
   - Home = dark; Visitor = white (Mod B)
   - Game = two 18-min halves (Mod A)
   - Bonus = 1&1 on 7th/half; 2-shot on 10th/half (Mod K) NOT quarter-based
   - Coaching box = 14 feet (Mod I)
   - No closely guarded on dribbler (Mod F)
   - Shot clock 35 seconds mandatory all varsity (Mod E)
   - Mercy rule: 35-pt lead, <9 min remaining = running clock (Mod G)
   - Restricted area arc required all levels (Mod H)
   - Apparel must be black or white (Mod C)
"""

# =============================================================================
# SYSTEM PROMPTS
# =============================================================================

SYSTEM_PROMPT = f"""You are RefBuddy — a straightforward, hyper-precise Minnesota high school basketball referee assistant.

You ONLY reference information from the CORE_KNOWLEDGE below. Cite page/rule number every time.
For video questions, first ask for transcription or key timestamps.
Never hallucinate MSHSL or NFHS mechanics.
Always ask clarifying questions on game context before ruling.

CRITICAL LAYERING RULE: The CORE_KNOWLEDGE contains a `2023-2024_NFHS_Basketball_Rulebook.md` baseline (Sections 1–9) plus a 2023–2026 changes section (Section 0) at the top.
- DEFAULT to the `2023-2024_NFHS_Basketball_Rulebook.md` for any rule not listed in Section 0.
- If Section 0 contains a change for that rule, APPLY the updated rule and cite the year: e.g., "[2025-26 change]" or "[2025-26 change — overrides Rule X-X-X]".
- MSHSL Minnesota Modifications ALWAYS override NFHS defaults. Always apply MSHSL mods for MSHSL games.
- If a rule was changed multiple times, apply the MOST RECENT version and note the history.

Your behavior:
1. Start EVERY response with the most relevant rule citation (e.g., "Rule 9-7 [Three Seconds]" or "MSHSL Mod K" or "MSHSL Shot Clock Protocol — Reset to 20") and include the year if the rule changed after 2023-24.
2. Reference personal game notes when applicable.
3. End EVERY response with: "*Not official MSHSL interpretation — confirm with your assignor.*"
4. Temperature = 0 mindset: maximum precision, no guessing, no hallucinating.
5. If game context (level, MSHSL vs. NFHS, crew size, quarter/half) is missing, ask before ruling.
6. For video/film analysis: always include a VISIBILITY CHECK section. Use "Frame N" format.
7. For RefGrade evaluations: structured scores (0-100), frame-by-frame highlights, visibility notes, "What to work on" bullets.

---
{CORE_KNOWLEDGE}
"""

REFGRADE_PROMPT = f"""You are RefBuddy acting as a professional officiating evaluator for Minnesota high school basketball.

Output EXACTLY this structure:

## 📊 RefGrade Report
**Clip:** [filename] | **Evaluated:** [scope] | **Frames:** [range] | **Date:** [today]

## 👁️ Visibility Check
List each position: CLEARLY VISIBLE (frames N...) / PARTIALLY VISIBLE (frames N-N) / NOT VISIBLE IN ANY FRAME

## 📈 Scores
| Category | Score | Notes |
|----------|-------|-------|
| Positioning | XX/100 | |
| Call Accuracy | XX/100 | |
| Mechanics Execution | XX/100 | |
| Dead-ball Officiating | XX/100 | |
| Communication/Signals | XX/100 | |
| **Overall** | **XX/100** | |

90-100=Excellent; 80-89=Good; 70-79=Average; 60-69=Needs work; <60=Significant concern

## 🎬 Frame-by-Frame Highlights
## ✅ Strengths
## 🔧 What to Work On
## 📋 Summary

*Not official MSHSL interpretation — confirm with your assignor.*

Cite NFHS rules and MSHSL mechanics on every observation. Never hallucinate.
{CORE_KNOWLEDGE}
"""

QUIZ_SYSTEM_PROMPT = f"""You are RefBuddy Quiz Engine — a precise question generator for Minnesota high school basketball officials.

ABSOLUTE RULES — violating these will cause test failures:
1. Respond with ONLY valid JSON. Zero preamble. Zero markdown fences. Zero trailing text.
2. Multiple-choice: EXACTLY 4 options (A, B, C, D). Exactly ONE correct answer.
3. True/False: EXACTLY 2 options: {{"A": "True", "B": "False"}}.
4. Mix types roughly 50% multiple_choice / 50% true_false. Vary the ratio naturally.
5. Questions must be CHALLENGING — not trivial. Use specific rule numbers, shot clock resets, timing rules, and realistic scenario language.
6. NEVER repeat the same topic, scenario, or rule in a batch. Cover wide breadth.
7. Distractors for MC must be plausible but clearly wrong to someone who studied.

Single question JSON structure:
{{
  "question": "Full question text — be specific and scenario-based when possible",
  "type": "multiple_choice",
  "options": {{"A": "option", "B": "option", "C": "option", "D": "option"}},
  "correct": "B",
  "explanation": "Thorough explanation: why correct answer is right, why each wrong answer is wrong, what the rule actually says.",
  "rule_citation": "Exact rule number or MSHSL Modification letter",
  "personal_note": "From your MSHSL Season X notes: [specific situation] (empty string if not applicable)",
  "topic": "Rules|Mechanics|Shot Clock|Positioning|Signals|Game Situations|MSHSL Specific|2025-26 Changes"
}}

True/False structure (type must be "true_false"):
{{
  "question": "True or False: [specific statement that requires knowledge to evaluate]",
  "type": "true_false",
  "options": {{"A": "True", "B": "False"}},
  "correct": "A",
  "explanation": "...",
  "rule_citation": "...",
  "personal_note": "",
  "topic": "Rules"
}}

For a BATCH of 10 questions: JSON array of 10 objects. Include:
- At least 2 MSHSL-specific questions (mercy rule, MN modifications, shot clock)
- At least 2 mechanics/positioning questions (Lead/Trail/Center responsibilities)
- At least 1 question on 2025-26 rule changes
- At least 1 scenario-based game situation question
- At least 1 question from personal game notes
- At least 1 shot clock reset scenario question
- The rest from NFHS rules (varied — not all from Rule 9)

{CORE_KNOWLEDGE}
"""

CREW_EVAL_PROMPT = f"""You are RefBuddy acting as a professional officiating evaluator for Minnesota high school basketball. You are analyzing game film to evaluate the officiating crew.

Generate a comprehensive crew evaluation report with the following structure:

## 📊 Crew Evaluation Report
**Game Film:** [filename] | **Date:** [today] | **Evaluated By:** RefBuddy

## 👁️ Visibility Check
For each crew position, note: CLEARLY VISIBLE (frames N...) / PARTIALLY VISIBLE / NOT VISIBLE — analysis inferred from play action

## 📈 Overall Crew Score: XX/100

## 📋 Per-Position Highlights
For each visible official (Lead/Trail/Center): what they did well, positioning observations, any missed calls or mechanics issues. Cite specific frames and NFHS/MSHSL rules.

## 🎬 Key Play Analysis
Walk through 3-5 significant plays/moments from the film with specific frame citations, what happened, what the correct mechanics called for, and how the officials responded.

## ✅ Crew Strengths

## 🔧 Areas for Development
Actionable bullets with specific mechanic/rule citations and suggested focus for next game.

## 📋 Summary

---
*Not official MSHSL interpretation — confirm with your MSHSL district assignor.*

Cite NFHS rules and MSHSL mechanics on every observation. Never hallucinate. Use "Frame N" format throughout.
{CORE_KNOWLEDGE}
"""

REF_EVAL_PROMPT = f"""You are RefBuddy acting as a professional officiating evaluator for Minnesota high school basketball. You are analyzing game film to evaluate ONE specific official.

Generate a focused evaluation report with the following structure:

## 📊 Official Evaluation Report
**Game Film:** [filename] | **Position Evaluated:** [position] | **Date:** [today]

## 👁️ Visibility Check
How clearly is this official visible in the provided frames? List specific frames where they appear.

## 📈 Position Score: XX/100

## 📐 Positioning Analysis
Was the official in the correct position for each situation? Cite specific frames. Reference MSHSL mechanics manual standards for this position (Lead/Trail/Center).

## 📋 Call Accuracy
Any whistles blown or situations where a whistle should have been blown. Was each decision correct per NFHS rules and MSHSL modifications? Cite Rule numbers and MSHSL Mods.

## ⚙️ Mechanics Execution
Signals, whistle timing, throw-in administration, FT administration, relay mechanics, communication. What was correct? What needs work?

## ✅ Strengths

## 🔧 Development Points
Specific, actionable improvements with exact mechanic citations and suggested drills.

## 📋 Summary

---
*Not official MSHSL interpretation — confirm with your MSHSL district assignor.*

Cite NFHS rules and MSHSL mechanics specifically. Use "Frame N" format. Never hallucinate.
{CORE_KNOWLEDGE}
"""

PREGAME_MEETING_PROMPT = f"""You are RefBuddy acting as a Minnesota high school basketball officiating coordinator.
Generate a CONCISE pre-game crew meeting agenda — maximum 1 to 1.5 printed pages.
Short bullet points only. No paragraphs. No explanations. No filler.
Each bullet must be actionable and specific. Cite rule numbers inline (e.g. MSHSL Mod G, Rule 9-7).
Total output should be ~300-400 words maximum.

Output EXACTLY this structure:

---
# Pre-Game Meeting Agenda
{{date}} | {{crew}} | {{level}}

## 2025-26 Rule Changes (know these cold)
- [list only the 2-3 most important 2025-26 changes with rule #]

## Key Mechanics Reminders
- [4-6 bullet points covering the highest-leverage mechanics for this crew size — Lead/Trail/Center specific]

## MSHSL Modifications to Confirm
- [3-4 critical MN mods that differ from NFHS — bonus system, home/visitor colors, closely guarded, mercy rule]

## Shot Clock Pre-Game
- [3-4 shot clock reminders — reset triggers, operator check, horn ≠ violation]

## Watch-Fors Tonight
- [3-5 specific situations from CORE_KNOWLEDGE most likely to come up]

## Assignor Notes
[ASSIGNOR_NOTES_PLACEHOLDER]

## Quick Scenarios (discuss briefly if time)
- [2 short scenario questions, one sentence each]

---
*Not official MSHSL interpretation.*

Keep it tight. Referees are reading this standing on a sideline before tip.
{CORE_KNOWLEDGE}
"""


# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="RefBuddy — MN HS Basketball",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# CSS — v1.0 Basketball Theme (same design system as Football v3.1)
# =============================================================================

BLUE   = "#003087"   # Deep navy
BLUE_L = "#1E56A0"
CREAM  = "#FAFAF7"
CARD   = "#FFFFFF"
BORDER = "#DDE3F0"
TEXT   = "#1F2937"
MUTED  = "#4B5563"
GREEN  = "#15803D"
AMBER  = "#92400E"
RED    = "#991B1B"

# Basketball court-inspired subtle SVG background
_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' width='120' height='120'>"
    "<rect width='120' height='120' fill='none'/>"
    # Court lines
    "<line x1='0' y1='60' x2='120' y2='60' stroke='%23003087' stroke-width='0.4' opacity='0.07'/>"
    "<line x1='60' y1='0' x2='60' y2='120' stroke='%23003087' stroke-width='0.4' opacity='0.07'/>"
    # Lane lines suggestion
    "<rect x='44' y='30' width='32' height='60' fill='none' stroke='%23003087' stroke-width='0.3' opacity='0.04'/>"
    # Half-court circle
    "<circle cx='60' cy='60' r='15' fill='none' stroke='%23003087' stroke-width='0.35' opacity='0.05'/>"
    # Basketball
    "<circle cx='60' cy='60' r='7' fill='none' stroke='%23003087' stroke-width='0.4' opacity='0.06'/>"
    "</svg>"
)
BG_URL = "data:image/svg+xml," + urllib.parse.quote(_SVG)

# ── Layer 1: Mandatory button + selectbox + sidebar + dark text ──────────────
st.markdown("""
<style>
    /* Light bg, black border, black text on ALL buttons */
    .stButton button, button, .stButton>button {
        color: #1F2937 !important;
        background-color: #F8FAFC !important;
        border: 2px solid #1F2937 !important;
        font-weight: 600;
    }
    .stButton button:hover { background-color: #E2E8F0 !important; }
    .stButton button:disabled, .stButton>button:disabled {
        background-color: #F1F5F9 !important;
        color: #94A3B8 !important;
        border-color: #94A3B8 !important;
    }
    /* Selectbox + multiselect — light bg, black border, black text */
    .stSelectbox > div, .stMultiSelect > div,
    .stSelectbox > div > div, .stMultiSelect > div > div {
        color: #1F2937 !important;
        background-color: #F8FAFC !important;
        border: 2px solid #1F2937 !important;
    }
    .stSelectbox label, .stMultiSelect label,
    [data-baseweb="select"] span, [data-baseweb="select"] div,
    [data-baseweb="popover"] li, [data-baseweb="menu"] li {
        color: #1F2937 !important;
        background-color: #F8FAFC !important;
    }
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #FFFFFF !important; }
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox,
    [data-testid="stSidebar"] .stTextInput,
    [data-testid="stSidebar"] .stMarkdown h1,
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div { color: #1F2937 !important; }
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="select"] span {
        color: #1F2937 !important; background-color: #F8FAFC !important;
    }
    /* Tab labels */
    .stTabs [data-baseweb="tab"] { color: #1F2937 !important; }
    .stTabs [aria-selected="true"] {
        color: #003087 !important; border-bottom: 3px solid #003087 !important;
    }
    /* Dark text everywhere */
    .stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown h1,
    .stMarkdown h2, .stMarkdown h3, .stMarkdown h4,
    .stMarkdown span, .stMarkdown strong, .stMarkdown em,
    p, span, label, h1, h2, h3, h4, h5,
    div[data-testid="stMarkdownContainer"] p,
    div[data-testid="stMarkdownContainer"] li,
    div[data-testid="stMarkdownContainer"] span,
    .stChatMessage p, .stChatMessage span, .stChatMessage li,
    [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessageContent"] span,
    [data-testid="stChatMessageContent"] li { color: #1F2937 !important; }
</style>
""", unsafe_allow_html=True)

# ── Layer 1b: Radio, inputs, sidebar, alerts ──────────────────────────────────
st.markdown("""
<style>
/* Radio labels */
.stRadio label, .stRadio label span, .stRadio label p,
div[data-testid="stRadio"] label span,
div[data-testid="stRadio"] label p,
.stRadio > div > label > div > p {
    color: #1F2937 !important;
    font-size: 0.95rem !important;
}
/* Chat input */
.stChatInput textarea, .stChatInput input {
    color: #1F2937 !important; background-color: #FFFFFF !important;
}
/* Text areas / inputs */
.stTextArea textarea, .stTextInput input {
    color: #1F2937 !important; background-color: #FFFFFF !important;
}
/* Select boxes */
[data-baseweb="select"] span, [data-baseweb="select"] div { color: #1F2937 !important; }
/* Sidebar */
[data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] div { color: #1F2937 !important; }
/* Alert boxes */
.stAlert p, .stAlert span, .stAlert div { color: #1F2937 !important; }
/* Expander headers */
.streamlit-expanderHeader p, .streamlit-expanderHeader span { color: #003087 !important; }
/* Caption */
.stCaption, .stCaption p { color: #4B5563 !important; }
</style>
""", unsafe_allow_html=True)

# ── Layer 2: Full theme CSS ───────────────────────────────────────────────────
st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{
    background-color: {CREAM};
    background-image: url("{BG_URL}");
    background-repeat: repeat;
    color: {TEXT};
    font-family: 'Inter', 'Segoe UI', sans-serif;
}}
.main .block-container {{ background: transparent; padding-top: 0.5rem; max-width: 1100px; }}

/* Sidebar */
[data-testid="stSidebar"] {{
    background-color: {CARD}; border-right: 2px solid {BORDER};
    box-shadow: 2px 0 8px rgba(0,48,135,0.06);
}}

/* Hero */
.home-hero {{ text-align: center; padding: 2.2rem 2rem 1.4rem 2rem; }}
.home-hero-title {{
    color: {BLUE} !important; font-size: 3.2rem; font-weight: 900;
    letter-spacing: -1.5px; margin: 0 0 0.2rem 0; line-height: 1.1;
}}
.home-hero-slogan {{ color: {MUTED}; font-size: 1.1rem; font-weight: 500; margin: 0 0 1.6rem 0; }}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{
    background-color: {CARD}; border-bottom: 2px solid {BORDER};
    border-radius: 8px 8px 0 0; gap: 2px; padding: 0 0.4rem;
}}
.stTabs [data-baseweb="tab"] {{
    color: {MUTED} !important; font-weight: 600; font-size: 0.9rem;
    padding: 0.55rem 1rem; border-radius: 6px 6px 0 0;
}}
.stTabs [aria-selected="true"] {{
    color: {BLUE} !important; background-color: {CREAM} !important;
    border-bottom: 3px solid {BLUE} !important;
}}

/* Cards */
.rb-card {{
    background: {CARD}; border: 1px solid {BORDER}; border-radius: 10px;
    padding: 1.2rem 1.4rem; margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,48,135,0.05); color: {TEXT};
}}
.rb-card-blue {{
    background: {CARD}; border-left: 4px solid {BLUE};
    border-radius: 0 10px 10px 0; padding: 1rem 1.2rem; margin-bottom: 0.8rem;
    box-shadow: 0 2px 8px rgba(0,48,135,0.05); color: {TEXT};
}}

/* Report output */
.report-output {{
    background: {CARD}; border: 2px solid {BORDER}; border-radius: 10px;
    padding: 1.6rem 2rem; margin-top: 1rem;
    box-shadow: 0 3px 12px rgba(0,48,135,0.07); color: {TEXT};
    line-height: 1.7; font-size: 0.93rem;
}}
.report-output h1, .report-output h2, .report-output h3, .report-output h4 {{
    color: {BLUE} !important;
}}

/* Quiz cards */
.quiz-question-card {{
    background: {CARD}; border: 2px solid {BORDER}; border-radius: 12px;
    padding: 1.5rem 1.8rem; margin-bottom: 1rem;
    box-shadow: 0 3px 12px rgba(0,48,135,0.08); color: {TEXT};
}}
.quiz-question-text {{
    font-size: 1.05rem; font-weight: 600; color: {TEXT} !important;
    line-height: 1.55; margin-bottom: 0.5rem;
}}
.quiz-result-correct {{
    background: #F0FDF4; border: 2px solid #4ADE80; border-radius: 8px;
    padding: 1rem 1.2rem; margin-top: 0.8rem; color: #14532D !important;
}}
.quiz-result-wrong {{
    background: #FFF1F2; border: 2px solid #F87171; border-radius: 8px;
    padding: 1rem 1.2rem; margin-top: 0.8rem; color: #7F1D1D !important;
}}
.quiz-explanation {{
    background: #EFF6FF; border-left: 4px solid {BLUE}; border-radius: 0 8px 8px 0;
    padding: 1rem 1.2rem; margin-top: 0.8rem; font-size: 0.92rem;
    line-height: 1.65; color: {TEXT} !important;
}}

/* Mode selector cards */
.mode-card-active {{
    background: #EEF2FF; border: 3px solid {BLUE}; border-radius: 12px;
    padding: 1.2rem 1.4rem; margin-bottom: 0.6rem;
    box-shadow: 0 4px 12px rgba(0,48,135,0.15); color: {TEXT};
}}
.mode-card-inactive {{
    background: {CARD}; border: 2px solid {BORDER}; border-radius: 12px;
    padding: 1.2rem 1.4rem; margin-bottom: 0.6rem;
    box-shadow: 0 2px 6px rgba(0,48,135,0.06); color: {TEXT};
}}

/* Pills */
.pill-ok {{
    display: inline-block; background: #DCFCE7; color: #166534;
    font-weight: 700; font-size: 0.78rem; border-radius: 20px;
    padding: 2px 10px; border: 1px solid #4ADE80;
}}
.pill-warn {{
    display: inline-block; background: #FEF3C7; color: #92400E;
    font-weight: 700; font-size: 0.78rem; border-radius: 20px;
    padding: 2px 10px; border: 1px solid #FCD34D;
}}
.pill-err {{
    display: inline-block; background: #FEE2E2; color: #991B1B;
    font-weight: 700; font-size: 0.78rem; border-radius: 20px;
    padding: 2px 10px; border: 1px solid #F87171;
}}
.pill-blue {{
    display: inline-block; background: #EEF2FF; color: {BLUE};
    font-weight: 700; font-size: 0.78rem; border-radius: 20px;
    padding: 2px 10px; border: 1px solid {BORDER};
}}

/* Misc */
.streamlit-expanderHeader {{
    background-color: #EEF2FF !important; color: {BLUE} !important;
    font-weight: 600 !important; border-radius: 8px !important;
}}
.rb-footer {{
    text-align: center; color: {MUTED}; font-size: 0.78rem;
    border-top: 1px solid {BORDER}; padding-top: 1rem; margin-top: 2.5rem;
}}
.ref-log {{
    background: #EEF2FF; border: 1px solid {BORDER};
    border-left: 4px solid {BLUE}; border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.1rem; font-size: 0.88rem; color: {TEXT};
}}
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
/* Keep header visible so the sidebar toggle chevron stays clickable,
   but hide the toolbar items we don't want (deploy, status, etc.) */
header {{ background: transparent !important; }}
[data-testid="stHeader"] {{ background: transparent !important; }}
[data-testid="stToolbar"] {{ visibility: hidden; }}
[data-testid="stDecoration"] {{ visibility: hidden; }}
[data-testid="stStatusWidget"] {{ visibility: hidden; }}
[data-testid="stSlider"] .st-by {{ background: {BLUE} !important; }}
[data-baseweb="select"] {{ background-color: {CARD} !important; }}
.stAlert {{ border-radius: 8px !important; font-size: 0.88rem !important; }}

/* Inputs */
.stTextArea textarea, .stTextInput input {{
    background-color: {CARD} !important; color: {TEXT} !important;
    border: 1.5px solid {BORDER} !important; border-radius: 8px !important;
    font-size: 0.92rem !important;
}}
.stTextArea textarea:focus, .stTextInput input:focus {{
    border-color: {BLUE} !important; box-shadow: 0 0 0 3px rgba(0,48,135,0.12) !important;
}}
[data-testid="stFileUploader"] {{
    border: 2px dashed {BLUE_L} !important; border-radius: 10px !important;
    background-color: #EEF2FF !important; padding: 0.5rem;
}}
.stChatMessage {{
    background: {CARD} !important; border: 1px solid {BORDER} !important;
    border-radius: 10px !important; margin-bottom: 0.5rem;
    box-shadow: 0 1px 4px rgba(0,48,135,0.06);
}}

/* Accuracy bar */
.accuracy-bar-wrap {{
    background: #E2E8F0; border-radius: 20px; height: 10px;
    margin: 6px 0 2px 0; overflow: hidden;
}}
.accuracy-bar-fill {{
    height: 10px; border-radius: 20px;
    background: linear-gradient(90deg, {BLUE} 0%, {BLUE_L} 100%);
    transition: width 0.4s ease;
}}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE
# =============================================================================

def _s(k, v):
    if k not in st.session_state:
        st.session_state[k] = v

_s("messages", [])
_s("uploaded_files_content", [])

# Film
_s("film_frames", [])
_s("film_frame_count", 0)
_s("film_video_name", "")
_s("film_fps_used", 1.0)
_s("film_analysis_result", "")

# RefGrade
_s("rg_frames", [])
_s("rg_frame_count", 0)
_s("rg_video_name", "")
_s("rg_fps_used", 1.0)
_s("rg_result", "")
_s("rg_saved_logs", [])

# Assignor Hub
_s("ah_sub", "crew")
_s("ah_crew_frames", [])
_s("ah_crew_frame_count", 0)
_s("ah_crew_video_name", "")
_s("ah_crew_result", "")
_s("ah_ref_frames", [])
_s("ah_ref_frame_count", 0)
_s("ah_ref_video_name", "")
_s("ah_ref_result", "")
_s("ah_pregame_result", "")
_s("ah_pregame_logs", [])

# Quiz
_s("quiz_mode", None)
_s("quiz_topic", "Mixed")
_s("quiz_current_q", None)
_s("quiz_answered", False)
_s("quiz_user_answer", None)
_s("quiz_total", 0)
_s("quiz_correct", 0)
_s("quiz_session_topics", [])
_s("tenq_questions", [])
_s("tenq_index", 0)
_s("tenq_answers", [])
_s("tenq_finished", False)
_s("tenq_answered_this", False)
_s("tenq_user_answer", None)
_s("quiz_log", [])


# =============================================================================
# HELPERS — Core
# =============================================================================

def b64(data: bytes) -> str:
    return base64.standard_b64encode(data).decode("utf-8")

MODEL = "claude-sonnet-4-20250514"

def make_client():
    """Create Anthropic client from Streamlit secrets."""
    key = None
    try:
        key = st.secrets["ANTHROPIC_API_KEY"]
    except (KeyError, AttributeError):
        pass
    if not key:
        try:
            key = st.secrets["anthropic"]["api_key"]
        except (KeyError, AttributeError):
            pass
    if not key:
        st.error(
            "❌ **ANTHROPIC_API_KEY not found in secrets.**\n\n"
            "Add it to `.streamlit/secrets.toml`:\n```\n"
            'ANTHROPIC_API_KEY = "sk-ant-..."\n```\n'
            "Or set it in the Streamlit Cloud dashboard under **Settings → Secrets**."
        )
        st.stop()
    return anthropic.Anthropic(api_key=key)

def api_key_ok() -> bool:
    return True

def handle_api_error(e: Exception) -> str:
    if isinstance(e, anthropic.AuthenticationError):
        return "❌ Authentication failed. Check ANTHROPIC_API_KEY in Streamlit secrets."
    if isinstance(e, anthropic.RateLimitError):
        return "⚠️ Rate limit reached. Wait a moment and try again."
    if isinstance(e, anthropic.APIConnectionError):
        return "❌ Connection error. Check your internet connection."
    if isinstance(e, anthropic.BadRequestError):
        return (f"❌ Request too large or malformed: {e}\n\n"
                "Try reducing the frame range or using 0.5 fps extraction.")
    return f"❌ Unexpected error: {e}"

def prepare_file_content(uf):
    data = uf.read()
    name = uf.name.lower()
    if name.endswith(".pdf"):
        return {"type": "document",
                "source": {"type": "base64", "media_type": "application/pdf", "data": b64(data)},
                "title": uf.name}
    if name.endswith((".jpg", ".jpeg")):
        return {"type": "image",
                "source": {"type": "base64", "media_type": "image/jpeg", "data": b64(data)}}
    if name.endswith(".png"):
        return {"type": "image",
                "source": {"type": "base64", "media_type": "image/png", "data": b64(data)}}
    if name.endswith(".txt"):
        return {"type": "text",
                "text": f"[File: {uf.name}]\n\n{data.decode('utf-8', errors='replace')}"}
    return None

def stream_chat(client, messages, files, system=None):
    sys_p = system or SYSTEM_PROMPT
    api_msgs = []
    for i, m in enumerate(messages):
        if m["role"] == "user" and i == len(messages) - 1 and files:
            blocks = list(files) + [{"type": "text", "text": m["content"]}]
            api_msgs.append({"role": "user", "content": blocks})
        else:
            api_msgs.append({"role": m["role"], "content": m["content"]})
    with client.messages.stream(
        model=MODEL, max_tokens=4096,
        system=sys_p, messages=api_msgs, temperature=0,
    ) as s:
        yield from s.text_stream

def call_api_sync(prompt: str, system: str, max_tokens: int = 3000) -> str:
    client = make_client()
    resp = client.messages.create(
        model=MODEL, max_tokens=max_tokens,
        system=system, messages=[{"role": "user", "content": prompt}], temperature=0,
    )
    return resp.content[0].text

def chat_log_json() -> str:
    return json.dumps({
        "exported_at": datetime.datetime.now().isoformat(),
        "model": MODEL,
        "messages": [{"role": m["role"], "content": m["content"],
                       "timestamp": m.get("timestamp", "")}
                     for m in st.session_state.messages],
    }, indent=2, ensure_ascii=False)


# =============================================================================
# HELPERS — Frame extraction
# =============================================================================

def extract_frames(video_path: str, fps: float = 1.0) -> list:
    """Extract frames from video at specified fps. Returns list of base64 JPEG strings."""
    if not OPENCV_AVAILABLE:
        raise RuntimeError("opencv-python-headless not available.")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")
    native_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    interval = max(1, int(round(native_fps / fps)))
    frames, idx = [], 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % interval == 0:
            h, w = frame.shape[:2]
            if w > 1280:
                frame = cv2.resize(frame, (1280, int(h * 1280 / w)), interpolation=cv2.INTER_AREA)
            ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if ok:
                frames.append(base64.standard_b64encode(buf).decode("utf-8"))
        idx += 1
    cap.release()
    return frames

def extract_video_uploaded(uploaded_video, fps: float = 1.0) -> tuple:
    suffix = ".mp4" if uploaded_video.name.lower().endswith(".mp4") else ".mov"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_video.read())
        tmp_path = tmp.name
    frames = extract_frames(tmp_path, fps=fps)
    os.unlink(tmp_path)
    return frames, uploaded_video.name

def build_vision_content(frames_b64, start_idx, end_idx, user_question,
                          video_name, fps_used, preamble_extra="") -> list:
    selected = frames_b64[start_idx: end_idx + 1]
    spf = 1.0 / fps_used
    content = [{"type": "text", "text": (
        f"Game film: {video_name}\n"
        f"Frames: {len(selected)} ({start_idx+1}–{end_idx+1} of {len(frames_b64)}) "
        f"at {fps_used} fps ({spf:.1f}s/frame).\n"
        f"Frame numbering is 1-based. Use 'Frame N' format.\n{preamble_extra}\n"
    )}]
    for i, fb in enumerate(selected):
        fn = start_idx + i + 1
        content.append({"type": "text", "text": f"--- Frame {fn} (~{(fn-1)/fps_used:.1f}s) ---"})
        content.append({"type": "image", "source": {"type": "base64",
                         "media_type": "image/jpeg", "data": fb}})
    content.append({"type": "text", "text": f"\nQuestion:\n{user_question}"})
    return content

def stream_vision(client, content_blocks, system):
    with client.messages.stream(
        model=MODEL, max_tokens=4096, system=system,
        messages=[{"role": "user", "content": content_blocks}], temperature=0,
    ) as s:
        yield from s.text_stream


# =============================================================================
# HELPERS — Quiz engine
# =============================================================================

def _strip_json_fences(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        parts = raw.split("```")
        raw = parts[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return raw.strip()

def generate_single_question(topic: str, used_topics: list = None) -> dict | None:
    if not api_key_ok():
        return None
    avoid_str = ""
    if used_topics and len(used_topics) > 0:
        recent = used_topics[-5:]
        avoid_str = (f"IMPORTANT: Do NOT generate a question about any of these topics "
                     f"that were just asked: {', '.join(recent)}. "
                     "Pick a completely different rule, mechanic, or scenario.\n")
    import random
    q_type_hint = "true_false" if random.random() < 0.5 else "multiple_choice"
    topic_str = "" if topic == "Mixed" else f"Topic focus: {topic}. "
    prompt = (
        f"{avoid_str}"
        f"{topic_str}"
        f"Generate one {q_type_hint} question for a Minnesota high school basketball referee. "
        f"It must be challenging, specific, and reference exact rule numbers or MSHSL modifications. "
        f"For multiple_choice: EXACTLY 4 options (A, B, C, D). "
        f"For true_false: EXACTLY 2 options (A=True, B=False). "
        f"Respond with ONLY valid JSON — no fences, no preamble."
    )
    try:
        client = make_client()
        resp = client.messages.create(
            model=MODEL, max_tokens=900,
            system=QUIZ_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        raw = _strip_json_fences(resp.content[0].text)
        q = json.loads(raw)
        if q.get("type") == "multiple_choice" and len(q.get("options", {})) != 4:
            return None
        if q.get("type") == "true_false" and len(q.get("options", {})) != 2:
            return None
        return q
    except Exception as e:
        st.error(f"❌ Failed to generate question: {e}")
        return None

def generate_ten_questions(topic: str) -> list | None:
    if not api_key_ok():
        return None
    topic_str = "" if topic == "Mixed" else f"Topic focus: {topic}. "
    prompt = (
        f"{topic_str}Generate exactly 10 questions for a Minnesota high school basketball referee. "
        "Mix: 5 multiple_choice (EXACTLY 4 options A/B/C/D each) + 5 true_false. "
        "Cover these areas: 2025-26 rule changes (no offensive goaltending, backboard slap), "
        "MSHSL mercy rule, MSHSL bonus system (1&1 half-based), shot clock resets (35/20), "
        "restricted area arc, flopping mechanics, Lead/Trail/Center positioning, "
        "throw-in spots (3-pt line rule), personal game note scenarios, closely guarded dribbling exception. "
        "Respond with ONLY a valid JSON array of 10 objects — no fences, no preamble."
    )
    try:
        client = make_client()
        resp = client.messages.create(
            model=MODEL, max_tokens=6000,
            system=QUIZ_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        raw = _strip_json_fences(resp.content[0].text)
        questions = json.loads(raw)
        if isinstance(questions, list) and len(questions) == 10:
            return questions
        if isinstance(questions, list) and len(questions) >= 5:
            return questions[:10]
        st.error("❌ Unexpected question count. Try again.")
        return None
    except Exception as e:
        st.error(f"❌ Failed to generate quiz: {e}")
        return None

def render_question_card(q: dict, question_num: str = ""):
    q_text = q.get("question", "")
    q_type = q.get("type", "multiple_choice")
    badge_color = "#EEF2FF"
    badge_label = "True/False" if q_type == "true_false" else "Multiple Choice"
    st.markdown(f"""
    <div class="quiz-question-card">
        <div class="quiz-question-text">{question_num} {q_text}
        <span style="background:{badge_color};color:{BLUE};font-size:0.72rem;
        font-weight:700;border-radius:20px;padding:2px 8px;margin-left:8px;">
        {badge_label}</span></div>
    </div>
    """, unsafe_allow_html=True)

def render_feedback(q: dict, user_answer: str) -> bool:
    correct = q.get("correct", "")
    options = q.get("options", {})
    correct_text = options.get(correct, correct)
    user_text = options.get(user_answer, user_answer)
    is_correct = user_answer == correct
    if is_correct:
        st.markdown(f"""<div class="quiz-result-correct">
        <strong>✅ Correct!</strong> &nbsp; {user_answer}: {user_text}
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="quiz-result-wrong">
        <strong>❌ Incorrect.</strong> You chose: {user_answer}: {user_text}<br>
        <strong>✔ Correct: {correct}: {correct_text}</strong>
        </div>""", unsafe_allow_html=True)
    explanation = q.get("explanation", "")
    rule_cite = q.get("rule_citation", "")
    personal = q.get("personal_note", "")
    pnote = f'<br><strong>📋 From your notes:</strong> {personal}' if personal else ""
    st.markdown(f"""<div class="quiz-explanation">
    <strong>📖 Explanation</strong><br>{explanation}<br><br>
    <strong>📌 Citation:</strong> {rule_cite}{pnote}
    </div>""", unsafe_allow_html=True)
    return is_correct

def accuracy_display(correct: int, total: int):
    pct = int(round(correct / total * 100)) if total > 0 else 0
    color = "#15803D" if pct >= 80 else ("#92400E" if pct >= 60 else "#991B1B")
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:12px;background:{CARD};
                border:1px solid {BORDER};border-radius:8px;padding:0.7rem 1rem;
                margin-bottom:0.8rem;">
        <div style="font-weight:800;font-size:1.4rem;color:{color};min-width:52px;">{pct}%</div>
        <div style="flex:1;">
            <div class="accuracy-bar-wrap">
                <div class="accuracy-bar-fill" style="width:{pct}%;background:{color};"></div>
            </div>
            <div style="font-size:0.8rem;color:{MUTED};margin-top:3px;">
                {correct} correct of {total} answered</div>
        </div>
    </div>""", unsafe_allow_html=True)


# =============================================================================
# HELPERS — Export (PDF + DOCX)
# =============================================================================

def sanitize_for_pdf(text: str) -> str:
    if not text:
        return ""
    replacements = {
        "\u2014": "-", "\u2013": "-", "\u2012": "-", "\u2015": "-",
        "\u2018": "'", "\u2019": "'", "\u201a": ",", "\u201b": "'",
        "\u201c": '"', "\u201d": '"', "\u201e": '"', "\u201f": '"',
        "\u2026": "...", "\u2022": "*", "\u2023": ">", "\u25e6": "o", "\u2043": "-",
        "\u00a0": " ", "\u200b": "", "\u200c": "", "\u200d": "", "\u2060": "", "\ufeff": "",
        "\u00d7": "x", "\u00f7": "/", "\u2212": "-", "\u00b0": "°",
        "\u2192": "->", "\u2190": "<-", "\u2194": "<->",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = text.encode("latin-1", errors="replace").decode("latin-1")
    return text.strip()

def markdown_to_pdf_bytes(md_text: str, title: str = "RefBuddy Report") -> bytes | None:
    try:
        from fpdf import FPDF
        L_MARGIN = 20; R_MARGIN = 20; TOP_MARGIN = 18; BOT_MARGIN = 15
        pdf = FPDF()
        pdf.set_margins(L_MARGIN, TOP_MARGIN, R_MARGIN)
        pdf.set_auto_page_break(auto=True, margin=BOT_MARGIN)
        pdf.add_page()
        eff_w = pdf.w - L_MARGIN - R_MARGIN
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 48, 135)
        pdf.multi_cell(eff_w, 7, sanitize_for_pdf(title), align="L")
        pdf.ln(1)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(107, 114, 128)
        date_str = sanitize_for_pdf(
            f"Generated: {datetime.datetime.now().strftime('%B %d, %Y %H:%M')}"
        )
        pdf.multi_cell(eff_w, 4, date_str, align="L")
        pdf.ln(2)
        pdf.set_draw_color(180, 200, 220)
        pdf.set_line_width(0.3)
        pdf.line(L_MARGIN, pdf.get_y(), pdf.w - R_MARGIN, pdf.get_y())
        pdf.ln(3)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(31, 41, 55)
        for raw_line in md_text.split("\n"):
            s = raw_line.strip()
            if not s:
                pdf.ln(2); continue
            if s == "---":
                pdf.ln(1)
                pdf.set_draw_color(200, 210, 220)
                pdf.line(L_MARGIN, pdf.get_y(), pdf.w - R_MARGIN, pdf.get_y())
                pdf.ln(2); continue
            if s.startswith("# ") or s.startswith("## "):
                pdf.ln(2)
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_text_color(0, 48, 135)
                pdf.multi_cell(eff_w, 6, sanitize_for_pdf(s.lstrip("#").strip()), align="L")
                pdf.set_font("Helvetica", "", 9); pdf.set_text_color(31, 41, 55); continue
            if s.startswith("### "):
                pdf.ln(1)
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(0, 48, 135)
                pdf.multi_cell(eff_w, 5, sanitize_for_pdf(s.lstrip("#").strip()), align="L")
                pdf.set_font("Helvetica", "", 9); pdf.set_text_color(31, 41, 55); continue
            if s.startswith("#### "):
                pdf.ln(1)
                pdf.set_font("Helvetica", "B", 9)
                pdf.set_text_color(31, 41, 55)
                pdf.multi_cell(eff_w, 5, sanitize_for_pdf(s.lstrip("#").strip()), align="L")
                pdf.set_font("Helvetica", "", 9); continue
            if s.startswith(("- ", "* ", "+ ")):
                content = sanitize_for_pdf(s[2:].replace("**", ""))
                pdf.set_x(L_MARGIN); pdf.cell(6, 4.5, "-")
                pdf.set_x(L_MARGIN + 6); pdf.multi_cell(eff_w - 6, 4.5, content, align="L"); continue
            import re as _re
            num_match = _re.match(r"^(\d+)\.\s+(.*)", s)
            if num_match:
                num = num_match.group(1) + "."; content = sanitize_for_pdf(num_match.group(2).replace("**", ""))
                pdf.set_x(L_MARGIN); pdf.cell(8, 4.5, num)
                pdf.set_x(L_MARGIN + 8); pdf.multi_cell(eff_w - 8, 4.5, content, align="L"); continue
            if s.startswith("| ") or (s.startswith("|") and "|" in s[1:]):
                stripped = s.replace("|", "").replace("-", "").replace(" ", "")
                if not stripped: continue
                row = sanitize_for_pdf(s.strip("|").replace("|", "  ").replace("**", ""))
                pdf.set_font("Courier", "", 8); pdf.multi_cell(eff_w, 4, row, align="L")
                pdf.set_font("Helvetica", "", 9); continue
            clean = sanitize_for_pdf(s.replace("**", "").replace("*", ""))
            pdf.multi_cell(eff_w, 4.5, clean, align="L")
        return bytes(pdf.output())
    except ImportError:
        return None

def markdown_to_docx_bytes(md_text: str, title: str = "RefBuddy Report") -> bytes | None:
    try:
        from docx import Document
        from docx.shared import Pt, RGBColor, Inches
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        doc = Document()
        for section in doc.sections:
            section.top_margin = Inches(1); section.bottom_margin = Inches(1)
            section.left_margin = Inches(1.2); section.right_margin = Inches(1.2)
        t_para = doc.add_paragraph()
        t_run = t_para.add_run(title)
        t_run.bold = True; t_run.font.size = Pt(18); t_run.font.color.rgb = RGBColor(0, 48, 135)
        t_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
        d_para = doc.add_paragraph()
        d_run = d_para.add_run(f"Generated: {datetime.datetime.now().strftime('%B %d, %Y %H:%M')}")
        d_run.font.size = Pt(9); d_run.font.color.rgb = RGBColor(107, 114, 128)
        doc.add_paragraph()
        for line in md_text.split("\n"):
            s = line.strip()
            if s.startswith("## ") or s.startswith("# "):
                h = doc.add_heading(s.lstrip("#").strip(), level=2)
                for run in h.runs: run.font.color.rgb = RGBColor(0, 48, 135)
            elif s.startswith("### "):
                h = doc.add_heading(s.lstrip("#").strip(), level=3)
                for run in h.runs: run.font.color.rgb = RGBColor(0, 48, 135)
            elif s.startswith(("- ", "* ")):
                p = doc.add_paragraph(style="List Bullet")
                p.add_run(s[2:].replace("**", "")).font.size = Pt(10)
            elif s == "---":
                doc.add_paragraph(); doc.add_paragraph().add_run("─" * 60).font.size = Pt(8); doc.add_paragraph()
            elif s == "":
                doc.add_paragraph()
            else:
                p = doc.add_paragraph(); p.add_run(s.replace("**", "")).font.size = Pt(10)
        buf = tempfile.NamedTemporaryFile(delete=False, suffix=".docx"); buf.close()
        doc.save(buf.name)
        with open(buf.name, "rb") as f: data = f.read()
        os.unlink(buf.name)
        return data
    except ImportError:
        return None


# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.markdown(
        '<div style="background:#F8FAFC;border:2px solid #1F2937;border-radius:8px;'
        'padding:0.7rem 1rem;margin-bottom:0.8rem;">'
        '<span style="color:#1F2937;font-weight:800;font-size:1.1rem;">🏀 RefBuddy</span><br>'
        '<span style="color:#4B5563;font-size:0.72rem;">Built by a ref for refs</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<span class="pill-ok">✅ claude-sonnet</span>',
        unsafe_allow_html=True,
    )
    st.caption("Powered by Anthropic")

    st.markdown("---")
    st.markdown("**Knowledge Base**")
    st.caption("NFHS Rulebook; MSHSL modifications: shot clock, restricted area; other state-specific rules; multiple seasons of game notes from veteran varsity officials")

    st.markdown("---")
    st.markdown("**Upload Files** *(Home chat)*")
    st.caption("PDFs, images, or TXT")
    chat_uploads = st.file_uploader(
        "chatfiles", type=["pdf", "jpg", "jpeg", "png", "txt"],
        accept_multiple_files=True, label_visibility="collapsed",
    )
    if chat_uploads:
        proc, names = [], []
        for uf in chat_uploads:
            c = prepare_file_content(uf)
            if c:
                proc.append(c); names.append(uf.name)
            else:
                st.warning(f"Unsupported: {uf.name}")
        st.session_state.uploaded_files_content = proc
        if names:
            st.markdown(f'<span class="pill-ok">✅ {len(names)} file(s)</span>', unsafe_allow_html=True)
    else:
        st.session_state.uploaded_files_content = []

    st.markdown("---")
    st.markdown("**Ref Log**")
    if st.session_state.messages:
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        st.download_button("⬇️ Download Chat Log", data=chat_log_json(),
                           file_name=f"refbuddy_bb_chat_{ts}.json",
                           mime="application/json", use_container_width=True)
    if st.button("🗑️ Clear Home Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")


# =============================================================================
# TABS
# =============================================================================

tab_home, tab_film, tab_grade, tab_ah, tab_quiz = st.tabs([
    "🏀 Home",
    "🎬 Game Film",
    "📊 RefGrade",
    "👥 Assignor Hub",
    "📝 Quiz & Drills",
])


# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — HOME
# ─────────────────────────────────────────────────────────────────────────────

with tab_home:
    st.markdown("""
    <div class="home-hero">
        <div class="home-hero-title">🏀 RefBuddy</div>
        <div class="home-hero-slogan">Built by a ref for refs</div>
    </div>
    """, unsafe_allow_html=True)

    chips = ["NFHS Rule Citations", "MSHSL Mods", "Shot Clock 35/20",
             "Lead · Trail · Center", "Restricted Arc", "Mercy Rule", "Quiz & Drills"]
    chip_html = " &nbsp; ".join(f'<span class="pill-blue">{c}</span>' for c in chips)
    st.markdown(f'<div style="text-align:center;margin-bottom:1.4rem;line-height:2.6;">'
                f'{chip_html}</div>', unsafe_allow_html=True)

    # Quick-start prompts
    if not st.session_state.messages:
        st.markdown(f'<p style="text-align:center;color:{MUTED};font-size:0.9rem;'
                    f'margin-bottom:0.8rem;"><em>Try one of these or type your own below</em></p>',
                    unsafe_allow_html=True)
        starter_qs = [
            "What is the MSHSL bonus free throw system — how is it different from NFHS?",
            "When is offensive goaltending a violation in 2025-26?",
            "Walk me through the shot clock reset when the offense gets the rebound.",
            "What is the MSHSL mercy rule and when does running clock start?",
            "Explain the restricted area arc rule and secondary defender definition.",
            "What are Lead, Trail, and Center responsibilities on free throws?",
            "When does MSHSL's closely guarded 5-second rule apply vs. not apply?",
            "What are the 2025-26 NFHS basketball rule changes I need to know?",
        ]
        c1, c2 = st.columns(2)
        for i, q in enumerate(starter_qs):
            col = c1 if i < 4 else c2
            with col:
                if st.button(f"➤ {q}", key=f"hq_{i}", use_container_width=True):
                    st.session_state.messages.append({
                        "role": "user", "content": q,
                        "timestamp": datetime.datetime.now().isoformat(),
                    })
                    st.rerun()

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🏀" if msg["role"] == "user" else "⚡"):
            st.markdown(msg["content"])

    # Stream assistant reply
    if (st.session_state.messages
            and st.session_state.messages[-1]["role"] == "user"):
        if not api_key_ok():
            st.warning("⚠️ Enter your Anthropic API key in the sidebar.")
        else:
            client = make_client()
            with st.chat_message("assistant", avatar="⚡"):
                ph = st.empty()
                full = ""
                try:
                    for chunk in stream_chat(
                        client,
                        st.session_state.messages,
                        st.session_state.uploaded_files_content,
                    ):
                        full += chunk
                        ph.markdown(full + "▌")
                    ph.markdown(full)
                    st.session_state.messages.append({
                        "role": "assistant", "content": full,
                        "timestamp": datetime.datetime.now().isoformat(),
                    })
                except Exception as e:
                    st.error(handle_api_error(e))

    # Chat input pinned to bottom
    user_in = st.chat_input(
        "Ask anything about NFHS/MSHSL basketball rules, shot clock, mechanics, or your notes…",
    )
    if user_in:
        st.session_state.messages.append({
            "role": "user", "content": user_in,
            "timestamp": datetime.datetime.now().isoformat(),
        })
        st.rerun()

    # Ref Log expander
    if st.session_state.messages:
        st.markdown("---")
        with st.expander("📋 Ref Log — Session Summary", expanded=False):
            st.markdown(f"""<div class="ref-log">
            <strong>Session Stats</strong><br>
            Messages: {len(st.session_state.messages)} &nbsp;|&nbsp;
            Model: {MODEL}<br>
            Started: {st.session_state.messages[0].get("timestamp","")[:19]}<br>
            Last: {st.session_state.messages[-1].get("timestamp","")[:19]}
            </div>""", unsafe_allow_html=True)
            for i, m in enumerate(st.session_state.messages):
                icon = "🏀 You" if m["role"] == "user" else "⚡ RefBuddy"
                st.markdown(f"**{icon}** _{m.get('timestamp','')[:19]}_")
                st.markdown(m["content"])
                if i < len(st.session_state.messages) - 1:
                    st.markdown("---")
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button("⬇️ Save Ref Log", data=chat_log_json(),
                               file_name=f"refbuddy_bb_reflog_{ts}.json",
                               mime="application/json")


# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — GAME FILM ANALYZER
# ─────────────────────────────────────────────────────────────────────────────

with tab_film:
    st.markdown("## 🎬 Game Film Analyzer")
    st.markdown("Upload a short clip. RefBuddy extracts frames with OpenCV and analyzes them "
                "for rule violations, mechanics, and positioning. **Always includes a Visibility Check.**")

    if not OPENCV_AVAILABLE:
        st.error("**opencv-python-headless is not installed.**\n\n"
                 "Run `pip install opencv-python-headless` then restart.")
        st.stop()

    st.markdown("### Step 1 — Upload Clip")
    st.info("Keep clips to 10–60 seconds. Trim to the specific play for best results.")
    film_vid = st.file_uploader("filmvid", type=["mp4", "mov"],
                                 label_visibility="collapsed", key="film_uploader")

    if film_vid:
        st.markdown("### Step 2 — Extraction Settings")
        fc1, fc2 = st.columns([1, 2])
        with fc1:
            fps_c = st.select_slider("fps_film", options=[0.5, 1.0, 2.0], value=1.0,
                                      help="0.5=overview | 1.0=standard | 2.0=fast action",
                                      key="film_fps")
            st.caption(f"30s clip at {fps_c} fps ≈ {int(30*fps_c)} frames")
        with fc2:
            st.info("Each frame ≈ 800–1,600 tokens. 30 frames ≈ $0.10–0.25.")

        st.markdown("### Step 3 — Extract Frames")
        if st.button("🎞️ Extract Frames", use_container_width=True, key="film_extract"):
            with st.spinner(f"Extracting at {fps_c} fps…"):
                try:
                    suffix = ".mp4" if film_vid.name.lower().endswith(".mp4") else ".mov"
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(film_vid.read()); tmp_path = tmp.name
                    frames = extract_frames(tmp_path, fps=fps_c)
                    os.unlink(tmp_path)
                    if not frames:
                        st.error("No frames extracted — check file format/codec.")
                    else:
                        st.session_state.film_frames = frames
                        st.session_state.film_frame_count = len(frames)
                        st.session_state.film_video_name = film_vid.name
                        st.session_state.film_fps_used = fps_c
                        st.session_state.film_analysis_result = ""
                        st.success(f"✅ {len(frames)} frames extracted from {film_vid.name}")
                except Exception as e:
                    st.error(f"❌ Extraction failed: {e}")

    if st.session_state.film_frame_count > 0:
        frames = st.session_state.film_frames
        n = st.session_state.film_frame_count
        fps_u = st.session_state.film_fps_used
        vname = st.session_state.film_video_name

        st.markdown("---")
        st.markdown(f"**{n} frames loaded** from `{vname}` — ~{n/fps_u:.0f}s of footage.")
        st.markdown("### Step 4 — Select Frame Range")
        if n == 1:
            sf, ef = 1, 1
        else:
            sf, ef = st.slider("filmrange", 1, n, (1, min(n, 30)), key="film_range")
        sel = ef - sf + 1
        st.caption(f"Frames {sf}–{ef} | {sel} frames | {(sf-1)/fps_u:.1f}s–{ef/fps_u:.1f}s")

        with st.expander(f"🔍 Preview {sel} selected frames", expanded=(sel <= 15)):
            prev = frames[sf-1:ef][:25]
            cols = st.columns(5)
            for i, fb in enumerate(prev):
                with cols[i % 5]:
                    st.image(base64.b64decode(fb), caption=f"F{sf+i} ~{(sf+i-1)/fps_u:.1f}s",
                             use_container_width=True)

        st.markdown("### Step 5 — Your Question")
        film_q = st.text_area("filmq_label", height=90,
                               placeholder="e.g. 'Is this a blocking foul or charge? Evaluate Lead position.' "
                                          "or 'Is the secondary defender outside the restricted arc?'",
                               label_visibility="collapsed", key="film_q")

        can_run = bool(film_q.strip())
        if st.button(f"🎬 Analyze {sel} Frames", disabled=not can_run,
                     use_container_width=True, key="film_run"):
            content_blocks = build_vision_content(
                frames, sf-1, ef-1, film_q, vname, fps_u,
                preamble_extra="Begin with VISIBILITY CHECK. Cite NFHS rules and MSHSL mechanics. Use Frame N format.")
            st.markdown("---"); st.markdown("#### 🎬 Film Analysis")
            client = make_client(); ph = st.empty(); full_film = ""
            try:
                with st.spinner(f"Analyzing {sel} frames… (15–60 seconds)"):
                    for chunk in stream_vision(client, content_blocks, SYSTEM_PROMPT):
                        full_film += chunk; ph.markdown(full_film + "▌")
                ph.markdown(full_film)
                st.session_state.film_analysis_result = full_film
            except Exception as e:
                st.error(handle_api_error(e))

        if st.session_state.film_analysis_result:
            st.markdown("---")
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("⬇️ Download Analysis (.txt)",
                                   data=st.session_state.film_analysis_result,
                                   file_name=f"film_analysis_{ts}.txt",
                                   mime="text/plain", use_container_width=True)
            with col2:
                pdf_b = markdown_to_pdf_bytes(st.session_state.film_analysis_result,
                                               "Film Analysis Report — RefBuddy Basketball")
                if pdf_b:
                    st.download_button("⬇️ Export PDF",
                                       data=pdf_b, file_name=f"film_analysis_{ts}.pdf",
                                       mime="application/pdf", use_container_width=True)
                else:
                    st.caption("💡 `pip install fpdf2` for PDF export")

    elif film_vid is None:
        st.markdown("---")
        st.markdown("""<div class="rb-card-blue">
        <h4 style="margin-top:0;color:#003087;">How Game Film Analyzer Works</h4>
        <ol style="color:#1F2937;line-height:2.0;">
        <li>Upload a .mp4 or .mov clip (10–60 seconds)</li>
        <li>Set extraction fps — 0.5 for overview, 1.0 standard, 2.0 for fast plays</li>
        <li>Extract Frames — OpenCV processes the clip</li>
        <li>Select frame range — focus on the key play</li>
        <li>Ask your question — block/charge? goaltending? positioning?</li>
        <li>Get frame-by-frame analysis with NFHS rules and MSHSL mechanic citations</li>
        </ol></div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — REFGRADE
# ─────────────────────────────────────────────────────────────────────────────

with tab_grade:
    st.markdown("## 📊 RefGrade — Officiating Evaluator")
    st.markdown("Upload game film to get a structured grade (0–100) on positioning, call accuracy, "
                "mechanics, dead-ball officiating, and communication.")

    if not OPENCV_AVAILABLE:
        st.error("**opencv-python-headless is required.** Run: `pip install opencv-python-headless`")
        st.stop()

    st.markdown("### Step 1 — Upload Clip")
    rg_vid = st.file_uploader("rgvid", type=["mp4", "mov"],
                               label_visibility="collapsed", key="rg_uploader")

    if rg_vid:
        st.markdown("### Step 2 — Evaluation Options")
        rc1, rc2 = st.columns(2)
        with rc1:
            eval_scope = st.selectbox("Evaluate for", options=[
                "Full Crew (Overall)", "Lead (L) — Under Basket",
                "Trail (T) — Half Court", "Center (C) — Middle"],
                key="rg_scope")
        with rc2:
            crew_size = st.selectbox("Crew size",
                                      options=["2-Person Crew", "3-Person Crew"],
                                      key="rg_crew_size")
        focus_input = st.text_input("Focus area (optional)",
                                     placeholder="e.g. 'Lead positioning on block/charge near restricted arc'",
                                     key="rg_focus")
        eval_categories = st.multiselect("Score these categories", options=[
            "Positioning", "Call Accuracy", "Mechanics Execution",
            "Dead-ball Officiating", "Communication / Signals",
            "Shot Clock Administration", "Free Throw Administration"],
            default=["Positioning", "Call Accuracy", "Mechanics Execution",
                     "Dead-ball Officiating", "Communication / Signals"],
            key="rg_categories")

        st.markdown("### Step 3 — Extract Frames")
        if st.button("🎞️ Extract Frames for RefGrade",
                     use_container_width=True, key="rg_extract"):
            with st.spinner("Extracting frames at 1 fps…"):
                try:
                    suffix = ".mp4" if rg_vid.name.lower().endswith(".mp4") else ".mov"
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(rg_vid.read()); tmp_path = tmp.name
                    frames = extract_frames(tmp_path, fps=1.0)
                    os.unlink(tmp_path)
                    if not frames:
                        st.error("No frames extracted.")
                    else:
                        st.session_state.rg_frames = frames
                        st.session_state.rg_frame_count = len(frames)
                        st.session_state.rg_video_name = rg_vid.name
                        st.session_state.rg_fps_used = 1.0
                        st.session_state.rg_result = ""
                        st.success(f"✅ {len(frames)} frames extracted from {rg_vid.name}")
                except Exception as e:
                    st.error(f"❌ Extraction failed: {e}")

    if st.session_state.rg_frame_count > 0:
        rg_frames = st.session_state.rg_frames
        rg_n = st.session_state.rg_frame_count
        rg_fps = st.session_state.rg_fps_used
        rg_vname = st.session_state.rg_video_name

        st.markdown("---")
        st.markdown(f"**{rg_n} frames loaded** from `{rg_vname}` — ~{rg_n/rg_fps:.0f}s of footage.")
        st.markdown("### Step 4 — Select Frame Range")
        if rg_n == 1:
            rg_sf = rg_ef = 1
        else:
            rg_sf, rg_ef = st.slider("rgrange", 1, rg_n, (1, min(rg_n, 30)), key="rg_range")
        rg_sel = rg_ef - rg_sf + 1
        st.caption(f"Frames {rg_sf}–{rg_ef} | {rg_sel} frames | "
                   f"{(rg_sf-1)/rg_fps:.1f}s–{rg_ef/rg_fps:.1f}s")

        with st.expander(f"🔍 Preview {rg_sel} selected frames", expanded=(rg_sel <= 15)):
            prev = rg_frames[rg_sf-1:rg_ef][:25]
            cols = st.columns(5)
            for i, fb in enumerate(prev):
                with cols[i % 5]:
                    st.image(base64.b64decode(fb),
                             caption=f"F{rg_sf+i} ~{(rg_sf+i-1)/rg_fps:.1f}s",
                             use_container_width=True)

        st.markdown("### Step 5 — Additional Notes (Optional)")
        rg_notes = st.text_area("rgnotes_label", height=80,
                                 placeholder="e.g. 'A whistle was blown on the drive — evaluate whether correct call and Lead position.'",
                                 label_visibility="collapsed", key="rg_notes")

        st.markdown("### Step 6 — Run RefGrade")
        can_grade = api_key_ok() and bool(eval_categories)
        if st.button(f"📊 Run RefGrade — {eval_scope} ({rg_sel} frames)",
                     disabled=not can_grade, use_container_width=True, key="rg_run"):
            cats_str = ", ".join(eval_categories)
            focus_str = f"\nFocus: {focus_input.strip()}" if focus_input.strip() else ""
            notes_str = f"\nContext: {rg_notes.strip()}" if rg_notes.strip() else ""
            rg_q = (f"RefGrade evaluation.\nClip: {rg_vname}\nScope: {eval_scope}\n"
                    f"Crew: {crew_size}\nScore: {cats_str}{focus_str}{notes_str}\n\n"
                    f"Use the exact RefGrade report structure. Begin with VISIBILITY CHECK. "
                    f"Cite every mechanic and NFHS/MSHSL rule.")
            content_blocks = build_vision_content(
                rg_frames, rg_sf-1, rg_ef-1, rg_q, rg_vname, rg_fps,
                preamble_extra="Structured RefGrade evaluation. Visibility Check is mandatory first section.")
            st.markdown("---"); st.markdown("#### 📊 RefGrade Report")
            client = make_client(); ph = st.empty(); full_grade = ""
            try:
                with st.spinner(f"Running RefGrade on {rg_sel} frames… (20–90 seconds)"):
                    for chunk in stream_vision(client, content_blocks, REFGRADE_PROMPT):
                        full_grade += chunk; ph.markdown(full_grade + "▌")
                ph.markdown(full_grade)
                st.session_state.rg_result = full_grade
                st.session_state.rg_saved_logs.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "clip": rg_vname, "scope": eval_scope,
                    "crew": crew_size, "frames": f"{rg_sf}-{rg_ef}", "result": full_grade,
                })
            except Exception as e:
                st.error(handle_api_error(e))

        if st.session_state.rg_result:
            st.markdown("---")
            cs1, cs2 = st.columns(2)
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            with cs1:
                st.download_button("⬇️ Download RefGrade (.txt)",
                                   data=st.session_state.rg_result,
                                   file_name=f"refgrade_{ts}.txt", mime="text/plain",
                                   use_container_width=True)
            with cs2:
                if st.session_state.rg_saved_logs:
                    st.download_button(f"⬇️ All Logs ({len(st.session_state.rg_saved_logs)})",
                                       data=json.dumps(st.session_state.rg_saved_logs, indent=2),
                                       file_name=f"refgrade_all_{ts}.json",
                                       mime="application/json", use_container_width=True)

    elif rg_vid is None:
        st.markdown("---")
        st.markdown("""<div class="rb-card-blue">
        <h4 style="margin-top:0;color:#003087;">How RefGrade Works</h4>
        <ol style="color:#1F2937;line-height:2.0;">
        <li>Upload a .mp4 or .mov clip (10–60 seconds)</li>
        <li>Choose scope — Full Crew or Lead / Trail / Center</li>
        <li>Select categories to score</li>
        <li>Extract Frames — always at 1 fps</li>
        <li>Set frame range — focus on the key sequence</li>
        <li>Run RefGrade — structured report with scores, frame citations, coaching bullets</li>
        </ol></div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — ASSIGNOR / CREW EVAL HUB
# ─────────────────────────────────────────────────────────────────────────────

with tab_ah:
    st.markdown("## 👥 Assignor / Crew Eval Hub")
    st.markdown("Film-based crew and individual official evaluations, plus auto-generated "
                "pre-game meeting agendas with PDF and Word export.")

    sub_c1, sub_c2, sub_c3 = st.columns(3)

    def _set_ah_sub(val):
        st.session_state.ah_sub = val

    with sub_c1:
        active = st.session_state.ah_sub == "crew"
        if st.button("🎬 Crew Eval", use_container_width=True,
                     key="ah_sub_crew",
                     type="primary" if active else "secondary"):
            _set_ah_sub("crew"); st.rerun()
        if active:
            st.markdown(f'<div style="height:3px;background:{BLUE};border-radius:2px;"></div>',
                        unsafe_allow_html=True)

    with sub_c2:
        active = st.session_state.ah_sub == "ref"
        if st.button("🧑‍⚖️ Ref Eval", use_container_width=True,
                     key="ah_sub_ref",
                     type="primary" if active else "secondary"):
            _set_ah_sub("ref"); st.rerun()
        if active:
            st.markdown(f'<div style="height:3px;background:{BLUE};border-radius:2px;"></div>',
                        unsafe_allow_html=True)

    with sub_c3:
        active = st.session_state.ah_sub == "pregame"
        if st.button("📅 Pre-Game Meeting", use_container_width=True,
                     key="ah_sub_pregame",
                     type="primary" if active else "secondary"):
            _set_ah_sub("pregame"); st.rerun()
        if active:
            st.markdown(f'<div style="height:3px;background:{BLUE};border-radius:2px;"></div>',
                        unsafe_allow_html=True)

    st.markdown("---")

    # ── SUB: CREW EVAL ──────────────────────────────────────────────────────

    if st.session_state.ah_sub == "crew":
        st.markdown("### 🎬 Crew Evaluation")
        st.markdown("Upload game film to get a full crew evaluation with positioning analysis, "
                    "call accuracy, and coaching bullets.")

        if not OPENCV_AVAILABLE:
            st.error("opencv-python-headless is required.")
        else:
            st.info("Supported: .mp4, .mov — shorter clips (10–120s) give the most focused analysis.")

            crew_vid = st.file_uploader("crew_vid", type=["mp4", "mov"],
                                         label_visibility="collapsed", key="ah_crew_uploader")

            if crew_vid:
                cv1, cv2 = st.columns(2)
                with cv1:
                    crew_fps = st.select_slider("crew_fps", options=[0.5, 1.0, 2.0], value=1.0,
                                                 key="crew_fps_slider")
                    st.caption(f"At {crew_fps} fps, a 60s clip → ~{int(60*crew_fps)} frames")
                with cv2:
                    crew_config = st.selectbox("Crew configuration",
                                                ["2-Person Crew", "3-Person Crew"],
                                                key="crew_config")

                crew_notes = st.text_area(
                    "Additional notes / assignor feedback (optional)", height=90,
                    placeholder=(
                        "e.g. 'Lead had a late whistle on a drive in Q2. "
                        "Focus on restricted area arc positioning and block/charge calls.' "
                        "Or leave blank for a general crew evaluation."
                    ),
                    key="crew_notes",
                )

                if st.button("🎞️ Extract Frames & Run Crew Evaluation",
                             use_container_width=True, key="crew_extract_run"):
                    with st.spinner(f"Extracting frames at {crew_fps} fps…"):
                        try:
                            suffix = ".mp4" if crew_vid.name.lower().endswith(".mp4") else ".mov"
                            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                                tmp.write(crew_vid.read()); tmp_path = tmp.name
                            frames = extract_frames(tmp_path, fps=crew_fps)
                            os.unlink(tmp_path)
                            if not frames:
                                st.error("No frames extracted.")
                            else:
                                st.session_state.ah_crew_frames = frames
                                st.session_state.ah_crew_frame_count = len(frames)
                                st.session_state.ah_crew_video_name = crew_vid.name
                                st.success(f"✅ {len(frames)} frames extracted. Running evaluation…")
                        except Exception as e:
                            st.error(f"❌ Extraction failed: {e}")
                            st.session_state.ah_crew_frame_count = 0

                    if st.session_state.ah_crew_frame_count > 0:
                        frames = st.session_state.ah_crew_frames
                        n = len(frames)
                        cap = min(n, 40)
                        notes_str = f"\nAssignor notes: {crew_notes.strip()}" if crew_notes.strip() else ""
                        crew_q = (
                            f"Please perform a full crew evaluation of this game film.\n"
                            f"Clip: {crew_vid.name}\n"
                            f"Crew configuration: {crew_config}\n"
                            f"Frames analyzed: 1–{cap} of {n} total{notes_str}\n\n"
                            f"Analyze all visible officials (Lead/Trail/Center) for positioning, call accuracy, "
                            f"mechanics execution, dead-ball officiating, shot clock administration, and communication. "
                            f"Provide specific frame citations throughout. "
                            f"Begin with a thorough VISIBILITY CHECK."
                        )
                        content_blocks = build_vision_content(
                            frames, 0, cap - 1, crew_q, crew_vid.name, crew_fps,
                            preamble_extra=(
                                "This is a full crew evaluation for Minnesota high school basketball. "
                                "Begin with VISIBILITY CHECK. "
                                "Analyze every visible official with specific frame citations. "
                                "Cite NFHS rules and MSHSL mechanics throughout."
                            )
                        )
                        st.markdown("---"); st.markdown("#### 📊 Crew Evaluation Report")
                        client = make_client(); ph = st.empty(); full_ce = ""
                        try:
                            with st.spinner(f"Analyzing {cap} frames for crew evaluation… (30–120 seconds)"):
                                for chunk in stream_vision(client, content_blocks, CREW_EVAL_PROMPT):
                                    full_ce += chunk; ph.markdown(full_ce + "▌")
                            ph.markdown(full_ce)
                            st.session_state.ah_crew_result = full_ce
                        except Exception as e:
                            st.error(handle_api_error(e))

            if st.session_state.ah_crew_result:
                st.markdown("---")
                with st.expander("📄 Crew Evaluation Report", expanded=True):
                    st.markdown(st.session_state.ah_crew_result)

                st.markdown("**Export Report**")
                ex1, ex2, ex3 = st.columns(3)
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                with ex1:
                    st.download_button("⬇️ Download TXT",
                                       data=st.session_state.ah_crew_result,
                                       file_name=f"crew_eval_{ts}.txt",
                                       mime="text/plain", use_container_width=True)
                with ex2:
                    pdf_b = markdown_to_pdf_bytes(st.session_state.ah_crew_result,
                                                   "Crew Evaluation Report — RefBuddy Basketball")
                    if pdf_b:
                        st.download_button("⬇️ Export PDF",
                                           data=pdf_b, file_name=f"crew_eval_{ts}.pdf",
                                           mime="application/pdf", use_container_width=True)
                    else:
                        st.caption("💡 `pip install fpdf2` for PDF export")
                with ex3:
                    if st.button("🗑️ Clear Report", use_container_width=True, key="crew_clear"):
                        st.session_state.ah_crew_result = ""
                        st.session_state.ah_crew_frame_count = 0; st.rerun()

    # ── SUB: REF EVAL ────────────────────────────────────────────────────────

    elif st.session_state.ah_sub == "ref":
        st.markdown("### 🧑‍⚖️ Individual Official Evaluation")
        st.markdown("Evaluate one specific official's positioning, mechanics, and call accuracy.")

        if not OPENCV_AVAILABLE:
            st.error("opencv-python-headless is required.")
        else:
            ref_vid = st.file_uploader("ref_vid", type=["mp4", "mov"],
                                        label_visibility="collapsed", key="ah_ref_uploader")

            if ref_vid:
                rv1, rv2 = st.columns(2)
                with rv1:
                    ref_position = st.selectbox("Position being evaluated",
                                                 ["Lead (L) — Under Basket",
                                                  "Trail (T) — Half Court",
                                                  "Center (C) — Middle"],
                                                 key="ref_pos_sel")
                with rv2:
                    ref_fps = st.select_slider("ref_fps", options=[0.5, 1.0, 2.0], value=1.0,
                                                key="ref_fps_slider")
                    st.caption(f"At {ref_fps} fps, a 60s clip → ~{int(60*ref_fps)} frames")

                ref_notes = st.text_area(
                    "Specific focus / assignor notes (optional)", height=80,
                    placeholder="e.g. 'Was the Lead in correct position for the block/charge at 0:45? "
                                "Evaluate restricted area arc awareness.'",
                    key="ref_notes",
                )

                if st.button("🎞️ Extract Frames & Run Ref Evaluation",
                             use_container_width=True, key="ref_extract_run"):
                    with st.spinner(f"Extracting frames at {ref_fps} fps…"):
                        try:
                            suffix = ".mp4" if ref_vid.name.lower().endswith(".mp4") else ".mov"
                            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                                tmp.write(ref_vid.read()); tmp_path = tmp.name
                            frames = extract_frames(tmp_path, fps=ref_fps)
                            os.unlink(tmp_path)
                            if not frames:
                                st.error("No frames extracted.")
                            else:
                                st.session_state.ah_ref_frames = frames
                                st.session_state.ah_ref_frame_count = len(frames)
                                st.session_state.ah_ref_video_name = ref_vid.name
                                st.success(f"✅ {len(frames)} frames extracted. Running evaluation…")
                        except Exception as e:
                            st.error(f"❌ Extraction failed: {e}")
                            st.session_state.ah_ref_frame_count = 0

                    if st.session_state.ah_ref_frame_count > 0:
                        frames = st.session_state.ah_ref_frames
                        n = len(frames)
                        cap = min(n, 40)
                        notes_str = f"\nFocus: {ref_notes.strip()}" if ref_notes.strip() else ""
                        ref_q = (
                            f"Please perform an individual evaluation of the {ref_position} official.\n"
                            f"Clip: {ref_vid.name}\n"
                            f"Position: {ref_position}\n"
                            f"Frames analyzed: 1–{cap} of {n} total{notes_str}\n\n"
                            f"Evaluate this official's positioning, call accuracy, mechanics execution, "
                            f"signal clarity, and communication. Provide specific frame citations. "
                            f"Begin with a VISIBILITY CHECK."
                        )
                        content_blocks = build_vision_content(
                            frames, 0, cap - 1, ref_q, ref_vid.name, ref_fps,
                            preamble_extra=(
                                f"Individual official evaluation — {ref_position}. "
                                "Minnesota high school basketball. Begin with VISIBILITY CHECK. "
                                "Cite NFHS rules and MSHSL mechanics throughout."
                            )
                        )
                        st.markdown("---"); st.markdown(f"#### 📊 {ref_position} Evaluation Report")
                        client = make_client(); ph = st.empty(); full_re = ""
                        try:
                            with st.spinner(f"Analyzing {cap} frames for {ref_position}… (30–120 seconds)"):
                                for chunk in stream_vision(client, content_blocks, REF_EVAL_PROMPT):
                                    full_re += chunk; ph.markdown(full_re + "▌")
                            ph.markdown(full_re)
                            st.session_state.ah_ref_result = full_re
                        except Exception as e:
                            st.error(handle_api_error(e))

            if st.session_state.ah_ref_result:
                st.markdown("---")
                with st.expander("📄 Individual Ref Evaluation Report", expanded=True):
                    st.markdown(st.session_state.ah_ref_result)

                st.markdown("**Export Report**")
                ex1, ex2, ex3 = st.columns(3)
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                with ex1:
                    st.download_button("⬇️ Download TXT",
                                       data=st.session_state.ah_ref_result,
                                       file_name=f"ref_eval_{ts}.txt",
                                       mime="text/plain", use_container_width=True)
                with ex2:
                    pdf_b = markdown_to_pdf_bytes(st.session_state.ah_ref_result,
                                                   "Individual Referee Evaluation Report — RefBuddy Basketball")
                    if pdf_b:
                        st.download_button("⬇️ Export PDF",
                                           data=pdf_b, file_name=f"ref_eval_{ts}.pdf",
                                           mime="application/pdf", use_container_width=True)
                    else:
                        st.caption("💡 `pip install fpdf2` for PDF export")
                with ex3:
                    if st.button("🗑️ Clear Report", use_container_width=True, key="ref_clear"):
                        st.session_state.ah_ref_result = ""
                        st.session_state.ah_ref_frame_count = 0; st.rerun()

    # ── SUB: PRE-GAME MEETING ─────────────────────────────────────────────────

    elif st.session_state.ah_sub == "pregame":
        st.markdown("### 📅 Pre-Game Meeting Agenda Generator")
        st.markdown(
            "Auto-generates a comprehensive pre-game agenda from CORE_KNOWLEDGE including "
            "2025-26 rule changes, MSHSL modifications, shot clock reminders, and mechanics. "
            "Add your own assignor notes for a fully customized meeting."
        )

        pg1, pg2 = st.columns(2)
        with pg1:
            pg_crew = st.selectbox("Crew size", ["2-Person Crew", "3-Person Crew"],
                                    key="pg_crew_sel")
            pg_level = st.selectbox("Game level",
                                     ["Varsity", "Junior Varsity", "9th Grade (Sub-Varsity)", "Playoff"],
                                     key="pg_level_sel")
        with pg2:
            pg_date = st.text_input("Game date (optional)",
                                     placeholder="e.g. Friday, January 16, 2026",
                                     key="pg_date")
            pg_teams = st.text_input("Teams (optional)",
                                      placeholder="e.g. Eden Prairie vs Wayzata",
                                      key="pg_teams")

        pg_focus = st.multiselect(
            "Additional emphasis topics (optional — will be included in agenda)",
            options=["2025-26 Rule Changes (No Offensive Goaltending, Backboard Slap)",
                     "Shot Clock Resets (35 vs 20 Scenarios)",
                     "Restricted Area Arc & Secondary Defender",
                     "Flopping Mechanics & Warning Protocol",
                     "Mercy Rule Procedure", "Overtime Procedure",
                     "Closely Guarded — MSHSL Dribbling Exception",
                     "Bonus Free Throw System (MSHSL 1&1 vs NFHS Quarter)",
                     "Throw-In Spots — 3-Point Line Demarcation",
                     "Uniform Compliance (Home=Dark, Visitor=White)",
                     "Free Throw Administration (C/L/T responsibilities)",
                     "Block/Charge — Restricted Area Signaling"],
            key="pg_focus_sel",
        )

        pg_assignor_notes = st.text_area(
            "Assignor's Custom Notes / Emphasis",
            height=130,
            placeholder=(
                "Add anything you want to emphasize for THIS specific game or crew:\n\n"
                "• 'This crew had timing issues last week — stress 5-second throw-in count'\n"
                "• 'Host school has a shot clock — confirm operator has recall function'\n"
                "• 'New official on crew (Trail) — walk through throw-in spot procedure'\n"
                "• 'Watch #32 on dark jerseys — has history of screens that flirt with illegal'\n"
                "• Any other game-specific or crew-specific notes..."
            ),
            key="pg_assignor_notes",
        )

        if st.button("📅 Generate Pre-Game Meeting Agenda",
                     use_container_width=True, key="pg_generate"):
            focus_str = (f"Additional emphasis topics requested: {', '.join(pg_focus)}\n"
                         if pg_focus else "")
            header_str = ""
            if pg_date or pg_teams:
                header_str = (f"Game: {pg_teams or 'TBD'} | "
                              f"Date: {pg_date or 'TBD'} | {pg_level}\n")

            if pg_assignor_notes.strip():
                raw_lines = [l.strip() for l in pg_assignor_notes.strip().splitlines() if l.strip()]
                if len(raw_lines) == 1:
                    notes_section = raw_lines[0]
                else:
                    notes_section = "\n".join(f"- {ln.lstrip('-* ').strip()}" for ln in raw_lines)
            else:
                notes_section = "(No specific assignor notes provided for this game.)"

            prompt = (
                f"Generate a pre-game meeting agenda for the following game.\n\n"
                f"{header_str}"
                f"Crew configuration: {pg_crew}\n"
                f"Game level: {pg_level}\n"
                f"{focus_str}\n"
                f"For the Assignor Notes section, use EXACTLY this content verbatim — "
                f"do not summarize or rephrase:\n"
                f"{notes_section}\n\n"
                f"Generate the full agenda following your system prompt structure. "
                f"Make all sections thorough and specific to basketball and MSHSL. "
                f"Assignor notes section must contain the notes exactly as written above."
            )

            with st.spinner("Generating pre-game meeting agenda… (15–30 seconds)"):
                try:
                    result = call_api_sync(prompt, PREGAME_MEETING_PROMPT, max_tokens=3000)
                    st.session_state.ah_pregame_result = result
                    st.session_state.ah_pregame_logs.append({
                        "timestamp": datetime.datetime.now().isoformat(),
                        "teams": pg_teams or "Unknown",
                        "date": pg_date or "Unknown",
                        "crew": pg_crew, "level": pg_level,
                        "result": result,
                    })
                    st.success("✅ Agenda generated!")
                except Exception as e:
                    st.error(handle_api_error(e))

        if st.session_state.ah_pregame_result:
            st.markdown("---")
            with st.expander("📋 Pre-Game Meeting Agenda", expanded=True):
                st.markdown(st.session_state.ah_pregame_result)

            st.markdown("**Export**")
            ep1, ep2, ep3, ep4 = st.columns(4)
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            with ep1:
                st.download_button("⬇️ TXT",
                                   data=st.session_state.ah_pregame_result,
                                   file_name=f"pregame_{ts}.txt",
                                   mime="text/plain", use_container_width=True)
            with ep2:
                pdf_b = markdown_to_pdf_bytes(st.session_state.ah_pregame_result,
                                               "Pre-Game Meeting Agenda — RefBuddy Basketball")
                if pdf_b:
                    st.download_button("⬇️ PDF",
                                       data=pdf_b, file_name=f"pregame_{ts}.pdf",
                                       mime="application/pdf", use_container_width=True)
                else:
                    st.caption("pip install fpdf2")
            with ep3:
                docx_b = markdown_to_docx_bytes(st.session_state.ah_pregame_result,
                                                 "Pre-Game Meeting Agenda — RefBuddy Basketball")
                if docx_b:
                    st.download_button("⬇️ Word",
                                       data=docx_b, file_name=f"pregame_{ts}.docx",
                                       mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                       use_container_width=True)
                else:
                    st.caption("pip install python-docx")
            with ep4:
                if st.button("🗑️ Clear", use_container_width=True, key="pg_clear"):
                    st.session_state.ah_pregame_result = ""; st.rerun()

            if st.session_state.ah_pregame_logs:
                st.markdown("---")
                st.markdown(f"**Agenda History ({len(st.session_state.ah_pregame_logs)} saved)**")
                for log in reversed(st.session_state.ah_pregame_logs[-5:]):
                    st.markdown(
                        f'<div class="rb-card" style="padding:0.7rem 1rem;">'
                        f'<strong>{log["teams"]}</strong> — {log["date"]} | {log["level"]} | {log["crew"]}'
                        f'<br><span style="font-size:0.78rem;color:{MUTED};">{log["timestamp"][:19]}</span>'
                        f'</div>', unsafe_allow_html=True
                    )
                ts2 = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    f"⬇️ Download All Agendas ({len(st.session_state.ah_pregame_logs)})",
                    data=json.dumps(st.session_state.ah_pregame_logs, indent=2, ensure_ascii=False),
                    file_name=f"pregame_all_{ts2}.json",
                    mime="application/json", use_container_width=True,
                )


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — QUIZ & DRILLS
# ─────────────────────────────────────────────────────────────────────────────

with tab_quiz:
    st.markdown("## 📝 Quiz & Drills")
    st.markdown("Test your knowledge of NFHS basketball rules, MSHSL modifications, shot clock, "
                "mechanics, and 2025-26 rule changes.")

    # Mode selector
    mode_c1, mode_c2 = st.columns(2)
    with mode_c1:
        active_flash = st.session_state.quiz_mode == "flashcard"
        if st.button(
            "⚡ Flashcard Mode\n\nOne question at a time — instant feedback",
            use_container_width=True, key="q_mode_flash",
            type="primary" if active_flash else "secondary",
        ):
            st.session_state.quiz_mode = "flashcard"
            st.session_state.quiz_current_q = None
            st.session_state.quiz_answered = False
            st.rerun()

    with mode_c2:
        active_10 = st.session_state.quiz_mode == "ten_questions"
        if st.button(
            "📋 10-Question Quiz\n\nFull quiz with score report and review",
            use_container_width=True, key="q_mode_10",
            type="primary" if active_10 else "secondary",
        ):
            st.session_state.quiz_mode = "ten_questions"
            st.session_state.tenq_questions = []
            st.session_state.tenq_index = 0
            st.session_state.tenq_answers = []
            st.session_state.tenq_finished = False
            st.session_state.tenq_answered_this = False
            st.session_state.tenq_user_answer = None
            st.rerun()

    st.markdown("---")

    # Topic selector
    quiz_topics = ["Mixed", "Rules (NFHS)", "MSHSL Specific", "Shot Clock",
                   "Mechanics & Positioning", "2025-26 Changes", "Restricted Area Arc",
                   "Fouls & Free Throws", "Game Situations"]
    if st.session_state.quiz_mode:
        st.session_state.quiz_topic = st.selectbox(
            "Topic Focus", quiz_topics, key="quiz_topic_sel"
        )

    # ── FLASHCARD MODE ─────────────────────────────────────────────────────────

    if st.session_state.quiz_mode == "flashcard":
        if st.session_state.quiz_total > 0:
            accuracy_display(st.session_state.quiz_correct, st.session_state.quiz_total)

        btn_label = "🔄 Next Question" if st.session_state.quiz_current_q else "🎯 Get Question"
        if st.button(btn_label, use_container_width=True, key="get_q_btn"):
            with st.spinner("Generating question…"):
                q = generate_single_question(
                    st.session_state.quiz_topic,
                    st.session_state.quiz_session_topics,
                )
            if q:
                st.session_state.quiz_current_q = q
                st.session_state.quiz_answered = False
                st.session_state.quiz_user_answer = None
                topic_tag = q.get("topic", "")
                if topic_tag:
                    st.session_state.quiz_session_topics.append(topic_tag)
                st.rerun()

        if st.session_state.quiz_current_q:
            q = st.session_state.quiz_current_q
            render_question_card(q)

            if not st.session_state.quiz_answered:
                options = q.get("options", {})
                option_labels = [f"{k}:  {v}" for k, v in sorted(options.items())]
                user_choice = st.radio("**Select your answer:**", option_labels, key="quiz_radio")
                if st.button("✅ Submit Answer", use_container_width=True, key="submit_q"):
                    chosen = user_choice.split(":")[0].strip()
                    st.session_state.quiz_user_answer = chosen
                    st.session_state.quiz_answered = True
                    is_correct = render_feedback(q, chosen)
                    st.session_state.quiz_total += 1
                    if is_correct:
                        st.session_state.quiz_correct += 1
                    st.rerun()
            else:
                render_feedback(q, st.session_state.quiz_user_answer)

        if st.session_state.quiz_total > 0:
            st.markdown("---")
            rc1, rc2 = st.columns(2)
            with rc1:
                if st.button("🗑️ Reset Score", use_container_width=True, key="reset_score"):
                    st.session_state.quiz_total = 0
                    st.session_state.quiz_correct = 0
                    st.session_state.quiz_current_q = None
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_session_topics = []
                    st.rerun()

    # ── 10-QUESTION MODE ───────────────────────────────────────────────────────

    elif st.session_state.quiz_mode == "ten_questions":
        if not st.session_state.tenq_questions and not st.session_state.tenq_finished:
            if st.button("🎯 Generate 10-Question Quiz", use_container_width=True, key="gen_10q"):
                with st.spinner("Generating 10 basketball rules questions… (20–40 seconds)"):
                    qs = generate_ten_questions(st.session_state.quiz_topic)
                if qs:
                    st.session_state.tenq_questions = qs
                    st.session_state.tenq_index = 0
                    st.session_state.tenq_answers = []
                    st.session_state.tenq_finished = False
                    st.session_state.tenq_answered_this = False
                    st.session_state.tenq_user_answer = None
                    st.rerun()

        elif st.session_state.tenq_questions and not st.session_state.tenq_finished:
            questions = st.session_state.tenq_questions
            total_qs = len(questions)
            idx = st.session_state.tenq_index

            st.markdown(f'<div style="text-align:right;color:{MUTED};font-size:0.88rem;margin-bottom:0.5rem;">'
                        f'Question {idx+1} of {total_qs} &nbsp;|&nbsp; Topic: {st.session_state.quiz_topic}</div>',
                        unsafe_allow_html=True)

            progress_pct = idx / total_qs
            st.markdown(f"""
            <div class="accuracy-bar-wrap">
                <div class="accuracy-bar-fill" style="width:{int(progress_pct*100)}%;"></div>
            </div>""", unsafe_allow_html=True)

            if idx < total_qs:
                q = questions[idx]
                options = q.get("options", {})
                render_question_card(q, question_num=f"Q{idx+1}.")

                if not st.session_state.tenq_answered_this:
                    option_labels = [f"{k}:  {v}" for k, v in sorted(options.items())]
                    user_choice = st.radio("**Select your answer:**", option_labels,
                                           key=f"tenq_radio_{idx}")
                    if st.button("✅ Submit Answer", use_container_width=True,
                                 key=f"tenq_submit_{idx}"):
                        chosen = user_choice.split(":")[0].strip()
                        st.session_state.tenq_user_answer = chosen
                        st.session_state.tenq_answered_this = True
                        is_correct = chosen == q.get("correct", "")
                        st.session_state.tenq_answers.append({
                            "question_num": idx + 1,
                            "user": chosen, "correct": q.get("correct", ""),
                            "is_correct": is_correct, "data": q,
                        })
                        st.rerun()
                else:
                    render_feedback(q, st.session_state.tenq_user_answer)
                    st.markdown("")
                    is_last = (idx == total_qs - 1)
                    btn_lbl = "📊 See Final Score" if is_last else f"➡️ Next ({idx+2}/{total_qs})"
                    if st.button(btn_lbl, use_container_width=True, key=f"tenq_next_{idx}"):
                        if is_last:
                            st.session_state.tenq_finished = True
                        else:
                            st.session_state.tenq_index += 1
                            st.session_state.tenq_answered_this = False
                            st.session_state.tenq_user_answer = None
                        st.rerun()

        elif st.session_state.tenq_finished and st.session_state.tenq_answers:
            answers = st.session_state.tenq_answers
            n_correct = sum(1 for a in answers if a["is_correct"])
            n_total = len(answers)
            pct = int(round(n_correct / n_total * 100))
            score_color = ("#15803D" if pct >= 80 else ("#92400E" if pct >= 60 else "#991B1B"))
            grade_label = ("🏆 Excellent!" if pct >= 90 else "✅ Good" if pct >= 80
                           else "📈 Getting there" if pct >= 70 else "📚 Keep studying"
                           if pct >= 60 else "🔁 Review the material")

            st.markdown(f"""
            <div style="background:{CARD};border:2px solid {score_color};border-radius:14px;
                        padding:2rem;text-align:center;margin-bottom:1.5rem;
                        box-shadow:0 4px 16px rgba(0,0,0,0.08);">
                <div style="font-size:3.5rem;font-weight:900;color:{score_color};">{pct}%</div>
                <div style="font-size:1.3rem;font-weight:700;color:#1F2937;margin:0.3rem 0;">
                    {n_correct} / {n_total} correct &nbsp; {grade_label}</div>
                <div style="color:{MUTED};font-size:0.9rem;">Topic: {st.session_state.quiz_topic}</div>
            </div>""", unsafe_allow_html=True)

            ra1, ra2 = st.columns(2)
            with ra1:
                if st.button("📁 Save Results to My Log", use_container_width=True, key="tenq_save"):
                    st.session_state.quiz_log.append({
                        "timestamp": datetime.datetime.now().isoformat(),
                        "topic": st.session_state.quiz_topic,
                        "score": pct, "correct": n_correct, "total": n_total,
                        "answers": answers,
                    })
                    st.success(f"✅ Saved! {len(st.session_state.quiz_log)} quiz log(s) on file.")
            with ra2:
                if st.button("🔄 Take Another Quiz", use_container_width=True, key="tenq_restart"):
                    st.session_state.tenq_questions = []
                    st.session_state.tenq_index = 0
                    st.session_state.tenq_answers = []
                    st.session_state.tenq_finished = False
                    st.session_state.tenq_answered_this = False
                    st.session_state.tenq_user_answer = None
                    st.rerun()

            st.markdown("---")
            st.markdown("### 📋 Full Review")
            for a in answers:
                qd = a["data"]
                opts = qd.get("options", {})
                u, c, ic = a["user"], a["correct"], a["is_correct"]
                icon = "✅" if ic else "❌"
                cbg = "#F0FDF4" if ic else "#FFF1F2"
                cbo = "#4ADE80" if ic else "#F87171"
                u_txt, c_txt = opts.get(u, u), opts.get(c, c)
                corr_line = (
                    "" if ic
                    else f'<br><strong style="color:#7F1D1D;">✔ Correct: {c}: {c_txt}</strong>'
                )
                st.markdown(f"""
                <div style="background:{cbg};border:1.5px solid {cbo};border-radius:10px;
                            padding:1.1rem 1.3rem;margin-bottom:0.9rem;">
                    <div style="font-weight:700;color:#1F2937;">
                        {icon} Q{a["question_num"]}: {qd.get("question","")}</div>
                    <div style="font-size:0.9rem;color:#1F2937;margin-top:0.3rem;">
                        <strong>Your answer:</strong> {u}: {u_txt}{corr_line}</div>
                </div>""", unsafe_allow_html=True)
                with st.expander(f"📖 Explanation — Q{a['question_num']}", expanded=False):
                    p = qd.get("personal_note", "")
                    pnote = f'<br><strong>📋 From your notes:</strong> {p}' if p else ""
                    st.markdown(f"""<div class="quiz-explanation">
                    {qd.get("explanation","")}<br><br>
                    <strong>📌 Citation:</strong> {qd.get("rule_citation","")}{pnote}
                    </div>""", unsafe_allow_html=True)

            if st.session_state.quiz_log:
                st.markdown("---")
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    f"⬇️ Download All Quiz Results ({len(st.session_state.quiz_log)} saved)",
                    data=json.dumps(st.session_state.quiz_log, indent=2, ensure_ascii=False),
                    file_name=f"refbuddy_bb_quiz_{ts}.json",
                    mime="application/json", use_container_width=True,
                )

    elif st.session_state.quiz_mode is None:
        st.markdown("""<div class="rb-card" style="text-align:center;padding:1.5rem;">
        <p style="color:#4B5563;margin:0;">👆 Select a mode above to get started.</p>
        </div>""", unsafe_allow_html=True)


# =============================================================================
# FOOTER
# =============================================================================

st.markdown(f"""
<div class="rb-footer">
    Built for referees, by a referee 🏀 &nbsp;|&nbsp;
    RefBuddy v1.0 &nbsp;|&nbsp; MN HS Basketball &nbsp;|&nbsp;
    NFHS Rulebook; MSHSL modifications: shot clock, restricted area; other state-specific rules; multiple seasons of game notes from veteran varsity officials<br>
    <span style="font-size:0.72rem;">
    Always confirm rulings with your MSHSL assignor. Not official MSHSL interpretation.
    </span>
</div>
""", unsafe_allow_html=True)
