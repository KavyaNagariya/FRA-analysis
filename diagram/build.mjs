import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import * as k from "file:///C:/Users/LENOVO/.gemini/config/plugins/anatomy/skills/anatomy/kit/iso-kit.mjs";
import { kitScript } from "file:///C:/Users/LENOVO/.gemini/config/plugins/anatomy/skills/anatomy/scripts/inline-kit.mjs";

const HERE = dirname(fileURLToPath(import.meta.url));

function build(theme = "dark") {
  const WIDTH = 680;
  const HEIGHT = 440;

  // 1. World Plans & Constants
  const PLATE = { x: -142, y: -68, w: 284, d: 136, r: 8 };
  const PLATE_H = 12;
  const FOOT_H = 6;

  // Transformer Cutaway Specimen (Left side: X = -94, Y = 0)
  const SPEC_X = -94;
  const SPEC_Y = 0;
  const RISER = { x: -122, y: -28, w: 56, d: 56, r: 3 };
  const RISER_H = 7;
  const YOKE_BOT = { x: -116, y: -22, w: 44, d: 44, r: 2 };
  const YOKE_BOT_H = 9; // Z: 7 to 16
  const CORE_R = 9.5;
  const CORE_Z0 = 16;
  const CORE_H = 54; // Z: 16 to 70

  const COIL_R = 14.8;
  const SP_R = 16.2;

  const YOKE_TOP = { x: -116, y: -22, w: 44, d: 44, r: 2 };
  const YOKE_TOP_Z = 70;
  const YOKE_TOP_H = 9; // Z: 70 to 79

  // Bushing (Z: 79 to 118)
  const TURRET_Z = 79;
  const TURRET_H = 5;
  const SHEDS = [
    { z: 84, r: 6.2, skirt_r: 11.5, h: 5 },
    { z: 89, r: 5.8, skirt_r: 10.5, h: 5 },
    { z: 94, r: 5.4, skirt_r: 9.5, h: 5 },
  ];
  const GLAND_Z = 99;
  const GLAND_H = 5;
  const BALL_Z = 104;
  const BALL_H = 4;

  // Dual Rails (spanning X = -50 to +120)
  const RAIL_FROM = -50;
  const RAIL_TO = 120;
  const RAIL_REAR_Y = -19;
  const RAIL_FRONT_Y = 15;
  const RAIL_W = RAIL_TO - RAIL_FROM;
  const RAIL_H = 4;

  // Carriage (Analyzer Sled)
  const CARRIAGE = { x: -24, y: -23, w: 48, d: 46, r: 2.5 };
  const CARRIAGE_Z = 3.5;
  const CARRIAGE_H = 6;
  const CARRIAGE_TOP = CARRIAGE_Z + CARRIAGE_H;

  // Dial Indicator on Carriage
  const DIAL_POST_Z = CARRIAGE_TOP;
  const DIAL_POST_H = 8.5;
  const DIAL_Z = DIAL_POST_Z + DIAL_POST_H;
  const DIAL_H = 9;
  const DIAL_TOP = DIAL_Z + DIAL_H;
  const DIAL_R = 17;

  // Deterministic Safety Floor Ratchet (Right side: X = 74, Y = -54)
  const RATCHET_BLOCK = { x: 74, y: -58, w: 38, d: 24, r: 2 };
  const RATCHET_H = 6;

  // Camera projection fitting
  const P = k.fitProjection(
    [
      ...k.boxCorners(PLATE, -PLATE_H - FOOT_H, 0),
      [SPEC_X - 25, SPEC_Y - 25, 0],
      [SPEC_X + 25, SPEC_Y + 25, BALL_Z + BALL_H + 2],
      [RAIL_TO + 10, RAIL_FRONT_Y + 10, DIAL_TOP + 5],
      [RATCHET_BLOCK.x + RATCHET_BLOCK.w, RATCHET_BLOCK.y, RATCHET_H + 12],
    ],
    WIDTH,
    HEIGHT,
    { pad: 26, azimuth: 42, elevation: 30 }
  );

  const at = (point) => k.iso(point, P);
  const S = (paths, style) => k.solidSvg(paths, style);
  const L = (d, style) => k.lineSvg(d, style);
  const D = (points, style) => k.dotsSvg(points, style);
  const byDepth = (points) => [...points].sort((a, b) => k.depthOf([a[0], a[1], 0], P) - k.depthOf([b[0], b[1], 0], P));

  // Vertical coil helper (since iso-kit coil only natively supports "x" and "y")
  function vcoil(cx, cy, z0, z1, r, turns) {
    const count = Math.round(turns * 24);
    const back = [];
    const front = [];
    let run = [];
    let near = null;
    const V = k.towardViewer(P);
    for (let index = 0; index <= count; index++) {
      const share = index / count;
      const angle = share * turns * Math.PI * 2;
      const point = at([cx + r * Math.cos(angle), cy + r * Math.sin(angle), z0 + (z1 - z0) * share]);
      const facing = Math.cos(angle) * V[0] + Math.sin(angle) * V[1] > 0;
      if (near === null) near = facing;
      if (facing !== near) {
        run.push(point);
        (near ? front : back).push(k.pathOf(run));
        run = [point];
        near = facing;
        continue;
      }
      run.push(point);
    }
    if (run.length > 1) (near ? front : back).push(k.pathOf(run));
    return { back: back.join(""), front: front.join("") };
  }

  // --- 1. Base Plate & Surroundings ---
  function basePlate() {
    const out = [`<path class="iso-halo" d="${k.haloOf(PLATE, -PLATE_H - FOOT_H, PLATE_H, P)}"/>`];

    // Feet sorted back to front
    for (const [x, y] of byDepth(k.corners(PLATE, 22))) {
      out.push(S(k.cylinder(x, y, 7.5, -PLATE_H - FOOT_H, 2, P, 28), { tone: "lo" }));
      out.push(S(k.cylinder(x, y, 5.5, -PLATE_H - FOOT_H + 2, FOOT_H - 2, P, 28), { tone: "mid" }));
    }

    // Heavy Granite Surface Slab
    out.push(S(k.slabOf(PLATE, -PLATE_H, PLATE_H, P, 8, 1.6), { tone: "mid" }));
    out.push(L(k.planOutline(k.insetPlan(PLATE, 5), 0, P), { tone: "lo" }));

    // 4 Corner Screws
    const screws = k.corners(PLATE, 11);
    out.push(L(screws.map(([x, y]) => k.ring(x, y, 2.4, 0, P, 16)).join(""), { tone: "lo" }));
    out.push(D(screws.map(([x, y]) => at([x, y, 0])), { size: 0.5 }));

    // Sub-Band Frequency Ruler Strip along front edge
    const strip = { x: -62, y: PLATE.y + PLATE.d - 14, w: 182, d: 7.5, r: 1.2 };
    out.push(S(k.slabOf(strip, 0, 0.7, P, 3), { tone: "lo", crease: "none" }));
    const ticks = k.topTicks(strip.x + 4, strip.x + strip.w - 4, 4, 5, strip.y + 0.8, 0.7, [1.8, 3.4], P);
    out.push(L(ticks.minor, { tone: "lo" }), L(ticks.major, { tone: "mid" }));

    // Sub-band divider lines on ruler (grounded on strip edges)
    const div1X = -12; // 2 kHz boundary
    const div2X = 52;  // 100 kHz boundary
    out.push(L(k.lineOnTop([div1X, strip.y], [div1X, strip.y + strip.d], 0.7, P), { tone: "hi" }));
    out.push(L(k.lineOnTop([div2X, strip.y], [div2X, strip.y + strip.d], 0.7, P), { tone: "hi" }));

    // Engraved Brass Certification Plate
    const label = { x: -134, y: 36, w: 62, d: 22, r: 1.5 };
    out.push(S(k.slabOf(label, 0, 0.8, P, 3), { tone: "mid", crease: "none" }));
    out.push(L(k.planOutline(k.insetPlan(label, 1.6), 0.8, P), { tone: "faint" }));
    out.push(L(k.lineOnTop([label.x + 6, label.y + 6], [label.x + label.w - 6, label.y + 6], 0.8, P), { tone: "lo", free: true }));
    out.push(L(k.lineOnTop([label.x + 6, label.y + 11], [label.x + label.w - 14, label.y + 11], 0.8, P), { tone: "lo", free: true }));
    out.push(L(k.lineOnTop([label.x + 6, label.y + 16], [label.x + label.w - 20, label.y + 16], 0.8, P), { tone: "lo", free: true }));
    out.push(D([at([label.x + 3, label.y + 11, 0.8]), at([label.x + label.w - 3, label.y + 11, 0.8])], { size: 0.45 }));
    out.push(k.faceTextSvg(k.topMatrix([label.x + 8, label.y + 7.5], 0.8, P, "x"), "IEEE C57.149 / IEC 60076", { size: 2.4, tone: "mid" }));

    return out.join("");
  }

  // --- 2. Transformer Cutaway Specimen Fixture ---
  function transformerSpecimen() {
    const out = [];

    // Specimen Riser Pedestal
    out.push(S(k.slabOf(RISER, 0, RISER_H, P, 4, 0.6), { tone: "mid" }));
    const riserScrews = k.corners(RISER, 4.5);
    out.push(D(riserScrews.map(([x, y]) => at([x, y, RISER_H])), { size: 0.45 }));

    // Bottom Laminated Silicon Steel Core Yoke (Low Band Inductance)
    out.push(S(k.slabOf(YOKE_BOT, RISER_H, YOKE_BOT_H, P, 4, 0.8), { tone: "mid" }));
    out.push(L(k.sideSeam(YOKE_BOT, RISER_H + 3, P), { tone: "faint" }));
    out.push(L(k.sideSeam(YOKE_BOT, RISER_H + 6, P), { tone: "faint" }));

    // Core Clamping Cross-Bars (Front & Back)
    for (const y of [-23, 19]) {
      out.push(S(k.slabOf({ x: -118, y, w: 48, d: 4, r: 1 }, RISER_H + 2, 5, P, 2, 0.4), { tone: "mid" }));
    }

    // 4 Vertical Core Tie-Rods with Hex Nuts
    const tieRods = [
      [-116, -21], [-72, -21],
      [-116, 21],  [-72, 21]
    ];
    for (const [x, y] of byDepth(tieRods)) {
      out.push(S(k.cylinder(x, y, 1.6, RISER_H + YOKE_BOT_H, YOKE_TOP_Z - (RISER_H + YOKE_BOT_H), P, 16), { tone: "mid", crease: "none" }));
      out.push(S(k.cylinder(x, y, 2.6, YOKE_TOP_Z + YOKE_TOP_H, 2.5, P, 16), { tone: "mid" }));
    }

    // Central Laminated Core Leg (Low Frequency < 2 kHz: Core Inductance)
    out.push(S(k.cylinder(SPEC_X, SPEC_Y, CORE_R, CORE_Z0, CORE_H, P, 36), { tone: "mid", crease: "none" }));
    out.push(L(k.sideArc(SPEC_X, SPEC_Y, CORE_R, 30, P, 24), { tone: "faint" }));
    out.push(L(k.sideArc(SPEC_X, SPEC_Y, CORE_R, 44, P, 24), { tone: "faint" }));
    out.push(L(k.sideArc(SPEC_X, SPEC_Y, CORE_R, 58, P, 24), { tone: "faint" }));

    // 5 Stacked Disc Windings with Radial Spacer Rings (Mid Frequency 2–100 kHz: Winding Structure)
    const discHeights = [19, 26.4, 33.8, 41.2, 48.6];
    discHeights.forEach((z0, i) => {
      // Disc Coil
      out.push(S(k.cylinder(SPEC_X, SPEC_Y, COIL_R, z0, 5.2, P, 44, 0.4), { tone: "hi", crease: "lo" }));
      const radTicks = k.radialTicks(SPEC_X, SPEC_Y, COIL_R - 0.4, 28, 4, z0 + 5.2, [0.8, 1.8], P);
      out.push(L(radTicks.minor, { tone: "lo" }), L(radTicks.major, { tone: "mid" }));

      // Spacer Comb Ring (between discs)
      if (i < 4) {
        out.push(S(k.cylinder(SPEC_X, SPEC_Y, SP_R, z0 + 5.2, 2.2, P, 36), { tone: "mid", crease: "none" }));
        out.push(L(k.sideArc(SPEC_X, SPEC_Y, SP_R, z0 + 6.3, P, 20), { tone: "faint" }));
      }
    });

    // Top Winding Compression Ring & Springs
    out.push(S(k.cylinder(SPEC_X, SPEC_Y, 15.5, 54.5, 3.5, P, 40, 0.4), { tone: "mid" }));
    for (const sy of [-8, 8]) {
      // Anchoring collars at top and bottom so coil ends land flush
      out.push(S(k.cylinder(SPEC_X, sy, 3.2, 58, 1.2, P, 16), { tone: "mid" }));
      out.push(S(k.cylinder(SPEC_X, sy, 3.2, YOKE_TOP_Z - 1.2, 1.2, P, 16), { tone: "mid" }));
      const sp = vcoil(SPEC_X, sy, 59.2, YOKE_TOP_Z - 1.2, 2.8, 4);
      out.push(L(sp.back, { tone: "lo" }));
      out.push(L(sp.front, { tone: "mid" }));
    }

    // Top Core Lamination Yoke
    out.push(S(k.slabOf(YOKE_TOP, YOKE_TOP_Z, YOKE_TOP_H, P, 4, 0.8), { tone: "mid" }));
    out.push(L(k.sideSeam(YOKE_TOP, YOKE_TOP_Z + 3, P), { tone: "faint" }));
    out.push(L(k.sideSeam(YOKE_TOP, YOKE_TOP_Z + 6, P), { tone: "faint" }));

    // High-Voltage Bushing & Terminal (High Frequency > 100 kHz: Leads & Bushing)
    out.push(S(k.cylinder(SPEC_X, SPEC_Y, 8.5, TURRET_Z, TURRET_H, P, 28), { tone: "mid" }));
    SHEDS.forEach((shed) => {
      out.push(S(k.cylinder(SPEC_X, SPEC_Y, shed.r, shed.z, shed.h, P, 24), { tone: "hi", crease: "lo" }));
      out.push(S(k.cylinder(SPEC_X, SPEC_Y, shed.skirt_r, shed.z + shed.h - 1.8, 1.8, P, 32, 0.3), { tone: "hi", crease: "lo" }));
    });
    out.push(S(k.cylinder(SPEC_X, SPEC_Y, 4.2, GLAND_Z, GLAND_H, P, 20), { tone: "hi" }));
    out.push(S(k.cylinder(SPEC_X, SPEC_Y, 3.2, BALL_Z, BALL_H, P, 18), { tone: "hi", lit: true }));
    out.push(D([at([SPEC_X, SPEC_Y, BALL_Z + BALL_H])], { size: 0.6, tone: "lit" }));

    // Ground Return Stud & Copper Strap
    const gndX = -70, gndY = 24;
    out.push(S(k.cylinder(gndX, gndY, 2.5, 0, 4.5, P, 16), { tone: "mid" }));
    out.push(S(k.slabOf({ x: -74, y: 14, w: 8, d: 12, r: 1 }, 2, 1.2, P, 2), { tone: "lo", crease: "none" }));

    return out.join("");
  }

  // --- 3. Dual Ground Chrome Guide Rails & Response Tracks ---
  function guideRails() {
    const out = [];

    // Left and Right Rail End Stops with socket cap screws (drawn before rails for proper seating)
    for (const x of [RAIL_FROM - 5, RAIL_TO]) {
      out.push(S(k.slabOf({ x, y: -23, w: 5, d: 44, r: 1.2 }, 0, 7.5, P, 3, 0.5), { tone: "mid" }));
      out.push(D([at([x + 2.5, RAIL_REAR_Y + 2.5, 7.5]), at([x + 2.5, RAIL_FRONT_Y + 2.5, 7.5])], { size: 0.45 }));
    }

    // Rear and Front Chrome Rails
    out.push(S(k.slabOf({ x: RAIL_FROM, y: RAIL_REAR_Y, w: RAIL_W, d: 5, r: 1 }, 0, RAIL_H, P, 3, 0.4), { tone: "mid" }));
    out.push(S(k.slabOf({ x: RAIL_FROM, y: RAIL_FRONT_Y, w: RAIL_W, d: 5, r: 1 }, 0, RAIL_H, P, 3, 0.4), { tone: "mid" }));

    // Central Leadscrew Drive Rod (solid slab that connects flush to both end stops)
    out.push(S(k.slabOf({ x: RAIL_FROM, y: -3.2, w: RAIL_W, d: 2.4, r: 1 }, 2, 2.4, P, 2, 0.3), { tone: "mid" }));

    // Milled Response Tracks between rails
    // Baseline Reference Track (top track)
    out.push(S(k.slabOf({ x: RAIL_FROM + 4, y: -10, w: RAIL_W - 8, d: 5.5, r: 1 }, 0, 1.4, P, 2), { tone: "mid", crease: "none" }));
    // Field Sweep Test Track (bottom track with resonance profile)
    out.push(S(k.slabOf({ x: RAIL_FROM + 4, y: 3, w: RAIL_W - 8, d: 5.5, r: 1 }, 0, 1.4, P, 2), { tone: "lo", crease: "none" }));

    return out.join("");
  }

  // --- 4. Deterministic Safety Floor Ratchet Mechanism ---
  function floorRatchet() {
    const out = [];

    // Base Mounting Block
    out.push(S(k.slabOf(RATCHET_BLOCK, 0, RATCHET_H, P, 3, 0.5), { tone: "mid" }));
    const screws = k.corners(RATCHET_BLOCK, 4);
    out.push(D(screws.map(([x, y]) => at([x, y, RATCHET_H])), { size: 0.4 }));

    // 4-Teeth Stepped Ratchet Quadrant Sector
    // Represents severity levels: 0 Healthy (top), 1 Warning, 2 Danger, 3 Critical (bottom)
    const notches = [
      { x: RATCHET_BLOCK.x + 6,  y: RATCHET_BLOCK.y + 5,  w: 24, d: 3.5, h: 5.5 },
      { x: RATCHET_BLOCK.x + 9,  y: RATCHET_BLOCK.y + 8.5, w: 21, d: 3.5, h: 4.2 },
      { x: RATCHET_BLOCK.x + 12, y: RATCHET_BLOCK.y + 12,  w: 18, d: 3.5, h: 3.0 },
      { x: RATCHET_BLOCK.x + 15, y: RATCHET_BLOCK.y + 15.5, w: 15, d: 3.5, h: 1.8 },
    ];
    notches.forEach((n) => {
      out.push(S(k.slabOf({ x: n.x, y: n.y, w: n.w, d: n.d, r: 0.8 }, RATCHET_H, n.h, P, 2), { tone: "hi", crease: "lo" }));
    });

    // Hardened Pawl Pivot Pin
    const pinX = RATCHET_BLOCK.x + 28, pinY = RATCHET_BLOCK.y + 19;
    out.push(S(k.cylinder(pinX, pinY, 2.2, RATCHET_H, 7, P, 16), { tone: "mid" }));

    // Safety Pawl Dog (Engaging the Floor Notch)
    out.push(S(k.slabOf({ x: pinX - 14, y: pinY - 2.5, w: 16, d: 5, r: 1 }, RATCHET_H + 4, 2.5, P, 2), { tone: "hi", lit: true }));

    // AI Rocker Beam (Free to escalate severity upwards, blocked from downgrading)
    out.push(S(k.slabOf({ x: RATCHET_BLOCK.x + 12, y: RATCHET_BLOCK.y + 7, w: 20, d: 4, r: 1 }, RATCHET_H + 7, 2.2, P, 2), { tone: "mid" }));

    // Return Spring anchored between spring pin and pawl lug
    const spX = pinX - 3, spY = pinY - 7;
    out.push(S(k.cylinder(spX, spY, 1.8, RATCHET_H, 1.5, P, 12), { tone: "mid" }));
    out.push(S(k.cylinder(spX, spY, 1.8, RATCHET_H + 6.5, 1.5, P, 12), { tone: "mid" }));
    const sp = vcoil(spX, spY, RATCHET_H + 1.5, RATCHET_H + 6.5, 1.4, 3);
    out.push(L(sp.back, { tone: "lo" }));
    out.push(L(sp.front, { tone: "mid" }));

    return out.join("");
  }

  // --- 5. Tuned Resonance Carriage (Analyzer Sled) ---
  function carriageSled() {
    const out = [`<path class="iso-halo" d="${k.haloOf(k.insetPlan(CARRIAGE, 2), CARRIAGE_Z, 0.1, P)}" style="filter:blur(4px)"/>`];

    // Main Carriage Chassis
    out.push(S(k.slabOf(CARRIAGE, CARRIAGE_Z, CARRIAGE_H, P, 5, 0.6), { tone: "mid" }));

    // 4 Bronze Flanged Sleeve Bushings
    const bushings = [
      [-16, RAIL_REAR_Y + 2.5], [16, RAIL_REAR_Y + 2.5],
      [-16, RAIL_FRONT_Y + 2.5], [16, RAIL_FRONT_Y + 2.5]
    ];
    bushings.forEach(([bx, by]) => {
      out.push(S(k.slabOf({ x: bx - 4.5, y: by - 4.5, w: 9, d: 9, r: 1.5 }, CARRIAGE_Z, CARRIAGE_H + 2, P, 3, 0.4), { tone: "hi" }));
      out.push(D([at([bx, by, CARRIAGE_TOP + 2])], { size: 0.4, tone: "lo" }));
    });

    // Front Knurled Positioning Knob
    const knob = [CARRIAGE.x + CARRIAGE.w / 2, CARRIAGE.y + CARRIAGE.d + 3.5];
    out.push(S(k.slabOf({ x: knob[0] - 2, y: CARRIAGE.y + CARRIAGE.d - 1, w: 4, d: 4, r: 1 }, CARRIAGE_Z + 1.2, 3.6, P, 2), { tone: "mid", crease: "none" }));
    out.push(S(k.cylinder(knob[0], knob[1], 4.2, CARRIAGE_Z, 6, P, 24), { tone: "mid" }));
    out.push(L(k.knurl(knob[0], knob[1], 4.2, CARRIAGE_Z, CARRIAGE_Z + 6, 24, P), { tone: "lo" }));

    // Dual Sensor Styluses:
    // Reference Stylus (rear) resting on Baseline Track
    out.push(S(k.cylinder(-4, -7.2, 1.4, 1.4, CARRIAGE_TOP - 1.4, P, 14), { tone: "mid" }));
    // Active Sensor Stylus (front) resting on Field Sweep Track
    out.push(S(k.cylinder(-4, 5.8, 1.6, 0.8, CARRIAGE_TOP - 0.8, P, 14), { tone: "hi", lit: true }));

    // Dial Gauge Mounting Pedestal
    out.push(S(k.cylinder(0, -2.5, 4.2, CARRIAGE_TOP, DIAL_POST_H, P, 20), { tone: "mid" }));
    out.push(L(k.sideArc(0, -2.5, 4.2, CARRIAGE_TOP + 4, P, 16), { tone: "faint" }));

    // BNC Coaxial Bulkhead Fitting on Sled
    out.push(S(k.cylinder(CARRIAGE.x + 6, CARRIAGE.y + 6, 2.4, CARRIAGE_TOP, 3.8, P, 14), { tone: "hi" }));

    // Dial Indicator Puck Body
    const [dx, dy] = [0, -2.5];
    out.push(S(k.cylinder(dx, dy, DIAL_R, DIAL_Z, DIAL_H, P, 64, 0.7), { tone: "hi", crease: "lo" }));
    out.push(L(k.knurl(dx, dy, DIAL_R, DIAL_TOP - 3.2, DIAL_TOP, 80, P, 0.3), { tone: "lo" }));
    out.push(L(k.sideArc(dx, dy, DIAL_R, DIAL_TOP - 3.2, P, 40), { tone: "faint" }));
    out.push(L(k.ring(dx, dy, DIAL_R - 2.2, DIAL_TOP, P, 64), { tone: "lo" }));

    // Radial Dial Face Graduations
    const dialTicks = k.radialTicks(dx, dy, DIAL_R - 3.2, 40, 5, DIAL_TOP, [1.3, 2.8], P);
    out.push(L(dialTicks.minor, { tone: "lo" }), L(dialTicks.major, { tone: "mid" }));
    out.push(L(k.ring(dx, dy, 1.8, DIAL_TOP, P, 16), { tone: "mid" }));
    out.push(k.faceTextSvg(k.topMatrix([dx, dy + 7.5], DIAL_TOP, P, "x"), "ΔdB · ρ", { size: 2.4, tone: "lo", anchor: "middle" }));

    return out.join("");
  }

  // Dial needle at deviation angle
  const needleAt = (devFraction) => {
    // 0 dev -> 12 o'clock (angle 0)
    // 20 dB dev -> full rotation
    const angle = devFraction * Math.PI * 2 - Math.PI / 2;
    const [dx, dy] = [0, -2.5];
    const tailX = dx - Math.cos(angle) * 3.2;
    const tailY = dy - Math.sin(angle) * 3.2;
    const tipX = dx + Math.cos(angle) * (DIAL_R - 4.2);
    const tipY = dy + Math.sin(angle) * (DIAL_R - 4.2);
    return k.lineOnTop([tailX, tailY], [tipX, tipY], DIAL_TOP + 0.2, P);
  };

  // Coaxial Injection Cable route
  function coaxialCables(carriageX) {
    const bncCarriage = at([carriageX + CARRIAGE.x + 6, CARRIAGE.y + 6, CARRIAGE_TOP + 3.8]);
    const bushingTop = at([SPEC_X, SPEC_Y, BALL_Z + BALL_H - 1]);
    const mid1 = at([(carriageX + SPEC_X) / 2 + 10, -20, 110]);
    const mid2 = at([(carriageX + SPEC_X) / 2 - 10, -10, 115]);

    const injectionWire = k.wireSvg(bncCarriage, bushingTop, {
      via: [mid1, mid2],
      tone: "mid",
      size: 1.1
    });

    return `<g data-part="wires">${injectionWire}</g>`;
  }

  // IEEE Sub-Band Calibrated Stops & Mock Profiles
  // Low Band (Core): X = -22, f = 400 Hz
  // Mid Band (Winding): X = 28, f = 28 kHz
  // High Band (Leads): X = 86, f = 450 kHz
  const STOPS = [
    { x: -22, band: "LF (420 Hz)", statusText: "Core Inductance", ccf: 0.942, dev: 3.8, status: "Warning" },
    { x: 28,  band: "MF (28 kHz)", statusText: "Winding Distortion", ccf: 0.742, dev: 14.8, status: "Critical" },
    { x: 86,  band: "HF (420 kHz)", statusText: "Bushing Lead", ccf: 0.891, dev: 5.7, status: "Warning" },
  ];

  const REACH = [-36, 104];
  const startStop = STOPS[1]; // default to Mid Band (Critical fault)

  const svg = k.figureSvg({
    width: WIDTH,
    height: HEIGHT,
    label:
      "SFRA Diagnostic Comparator on a granite surface plate. A cutaway transformer core and disc winding specimen is excited by a sweep frequency generator. A tuned resonance carriage slides along dual chrome rails across three IEEE Std C57.149 sub-bands (Low: Core, Mid: Winding, High: Leads). A differential dial gauge measures magnitude deviation and cross-correlation, while a hardened ratchet mechanism physically enforces the deterministic safety floor.",
    body: [
      basePlate(),
      transformerSpecimen(),
      guideRails(),
      floorRatchet(),
      `<g data-part="carriage" transform="${k.translateAlong(P, [startStop.x, 0, 0])}">
        ${carriageSled()}
        <path data-part="needle" class="iso-line" data-tone="lit" data-free="start" d="${needleAt(startStop.dev / 20)}" style="stroke-width:1.2"/>
      </g>`,
      coaxialCables(startStop.x),
    ],
  });

  const live = `
const P = ${JSON.stringify(P)};
const STOPS = ${JSON.stringify(STOPS)};
const REACH = ${JSON.stringify(REACH)};
const CARRIAGE_TOP = ${CARRIAGE_TOP};
const CARRIAGE = ${JSON.stringify(CARRIAGE)};
const DIAL_TOP = ${DIAL_TOP};
const DIAL_R = ${DIAL_R};
const SPEC_X = ${SPEC_X}, SPEC_Y = ${SPEC_Y}, BALL_Z = ${BALL_Z}, BALL_H = ${BALL_H};

const stage = document.querySelector(".iso-stage");
const svg = stage.querySelector("svg");
const carriage = svg.querySelector('[data-part="carriage"]');
const needle = svg.querySelector('[data-part="needle"]');
const wirePath = svg.querySelector('[data-part="wires"] path');
const wireEnds = svg.querySelectorAll('[data-part="wires"] circle');
const readout = document.querySelector("[data-readout]");
const still = matchMedia("(prefers-reduced-motion: reduce)");

const clamp = (v, min, max) => Math.min(max, Math.max(min, v));

const needleAt = ${needleAt.toString().replace("k.lineOnTop", "lineOnTop")};

// Continuous sub-band physics evaluation based on X position
function evaluateAt(cx) {
  if (cx < -12) {
    const t = clamp((cx - (-36)) / 24, 0, 1);
    const f = Math.round(40 + t * 1800);
    const dev = 2.0 + 3.5 * Math.sin(t * Math.PI);
    const ccf = 0.98 - 0.05 * Math.sin(t * Math.PI);
    const status = ccf >= 0.98 ? "Healthy" : (ccf >= 0.90 ? "Warning" : "Danger");
    return { band: "LF (" + (f < 1000 ? f + " Hz" : (f / 1000).toFixed(1) + " kHz") + ")", dev: dev.toFixed(1), ccf: ccf.toFixed(3), status };
  } else if (cx < 52) {
    const t = clamp((cx - (-12)) / 64, 0, 1);
    const f = (2.0 + t * 98.0).toFixed(1);
    const dev = 3.5 + 11.5 * Math.sin(t * Math.PI);
    const ccf = 0.95 - 0.22 * Math.sin(t * Math.PI);
    const status = ccf < 0.80 ? "Critical" : (ccf < 0.90 ? "Danger" : "Warning");
    return { band: "MF (" + f + " kHz)", dev: dev.toFixed(1), ccf: ccf.toFixed(3), status };
  } else {
    const t = clamp((cx - 52) / 52, 0, 1);
    const f = Math.round(100 + t * 900);
    const dev = 2.2 + 4.2 * Math.sin(t * Math.PI);
    const ccf = 0.96 - 0.08 * Math.sin(t * Math.PI);
    const status = ccf >= 0.90 ? "Warning" : "Danger";
    return { band: "HF (" + f + " kHz)", dev: dev.toFixed(1), ccf: ccf.toFixed(3), status };
  }
}

function updateWire(cx) {
  if (!wirePath || wireEnds.length < 2) return;
  const p0 = iso([cx + CARRIAGE.x + 6, CARRIAGE.y + 6, CARRIAGE_TOP + 3.8], P);
  const p1 = iso([(cx + SPEC_X) / 2 + 10, -20, 110], P);
  const p2 = iso([(cx + SPEC_X) / 2 - 10, -10, 115], P);
  const p3 = iso([SPEC_X, SPEC_Y, BALL_Z + BALL_H - 1], P);
  wirePath.setAttribute("d", pathOf([p0, p1, p2, p3]));
  wireEnds[0].setAttribute("cx", p0[0].toFixed(1));
  wireEnds[0].setAttribute("cy", p0[1].toFixed(1));
  wireEnds[1].setAttribute("cx", p3[0].toFixed(1));
  wireEnds[1].setAttribute("cy", p3[1].toFixed(1));
}

let x = ${startStop.x}, target = x;
let frame = 0, last = 0, clock = 0, touring = true, visible = false, idleTimer = 0;

const tourAt = (t) => {
  const index = Math.floor(t / 3.0) % STOPS.length;
  return STOPS[index].x;
};

function draw() {
  carriage.setAttribute("transform", translateAlong(P, [x, 0, 0]));
  updateWire(x);
  const state = evaluateAt(x);
  needle.setAttribute("d", needleAt(parseFloat(state.dev) / 20));

  const text = state.band + " · ΔdB: " + state.dev + " · CCF: " + state.ccf + " · [" + state.status.toUpperCase() + "]";
  if (readout.textContent !== text) readout.textContent = text;
  stage.setAttribute("aria-valuenow", state.dev);
  stage.setAttribute("aria-valuetext", text);
}

function tick(now) {
  const dt = last ? Math.min((now - last) / 1000, 1 / 30) : 1 / 60;
  last = now;
  const calm = still.matches;
  if (touring) {
    clock += dt;
    target = tourAt(clock);
  }
  x = calm ? target : x + (target - x) * (1 - Math.exp(-dt / 0.28));
  if (Math.abs(target - x) < 0.05) x = target;
  draw();

  const settled = !touring && Math.abs(x - target) < 0.05;
  frame = visible && !settled ? requestAnimationFrame(tick) : 0;
}

const run = () => { if (!frame && visible) { last = 0; frame = requestAnimationFrame(tick); } };
const steer = (next) => {
  touring = false;
  target = clamp(next, REACH[0], REACH[1]);
  clearTimeout(idleTimer);
  idleTimer = setTimeout(() => { touring = !still.matches; clock = 0; run(); }, 4200);
  run();
};

new IntersectionObserver((entries) => {
  visible = entries[entries.length - 1].isIntersecting;
  if (visible) run();
}, { rootMargin: "120px 0px" }).observe(stage);

if (still.matches) touring = false;

stage.addEventListener("pointermove", (event) => {
  const box = svg.getBoundingClientRect();
  const share = clamp(((event.clientX - box.left) / box.width - 0.28) / 0.54, 0, 1);
  steer(REACH[0] + share * (REACH[1] - REACH[0]));
});

stage.addEventListener("pointerleave", () => steer(target));

stage.addEventListener("keydown", (event) => {
  const here = STOPS.reduce((best, s, i) => (Math.abs(s.x - target) < Math.abs(STOPS[best].x - target) ? i : best), 0);
  let to = null;
  if (event.key === "ArrowRight" || event.key === "ArrowUp") to = Math.min(STOPS.length - 1, here + 1);
  if (event.key === "ArrowLeft" || event.key === "ArrowDown") to = Math.max(0, here - 1);
  if (event.key === "Home") to = 0;
  if (event.key === "End") to = STOPS.length - 1;
  if (to === null) return;
  event.preventDefault();
  steer(STOPS[to].x);
});

draw();
`;

  const body = k.plateHtml({
    fig: "Fig 1",
    title: "SFRA Diagnostic Comparator",
    hint: "Hover or arrow keys to sweep",
    readout: `${startStop.band} · ΔdB: ${startStop.dev} · CCF: ${startStop.ccf} · [${startStop.status.toUpperCase()}]`,
    keys: [
      { mark: "lit", label: "Active resonance stylus & dial needle measuring live sub-band deviation (ΔdB)" },
      { mark: "raised", label: "Transformer cutaway specimen (Low: core, Mid: disk winding, High: porcelain bushing)" },
      { mark: "mid", label: "Deterministic safety floor ratchet preventing ML severity downgrades" },
    ],
    caption:
      "A Sweep Frequency Response Analysis (SFRA) comparator bench grounded in IEEE Std C57.149™ and IEC 60076-18. As the tuned resonance carriage sweeps along the logarithmic guide rails, the dual-stylus sensor measures localized resonance shifts against the healthy baseline template. A differential dial gauge displays magnitude deviation, and the spring-loaded ratchet interlock enforces a deterministic safety floor: machine learning classifiers may escalate risk upon anomalous spectral detection, but cannot downgrade a physically deviant sub-band signature.",
    body: `<div class="iso-stage" tabindex="0" role="slider" aria-label="SFRA Diagnostic Comparator: sweep frequency bands from 20 Hz to 1 MHz" aria-valuemin="0" aria-valuemax="20" aria-valuenow="${startStop.dev}">${svg}</div>`,
  });

  const outHtml = k.pageHtml({
    title: "SFRA Diagnostic Comparator · IEEE C57.149",
    theme,
    body,
    script: kitScript() + live,
  });

  const fileName = theme === "light" ? "sfra-comparator-light.html" : "sfra-comparator.html";
  writeFileSync(join(HERE, fileName), outHtml);
  console.log(`Wrote ${join(HERE, fileName)}`);

  // Also write to app/static/diagram/
  const staticDir = join(HERE, "..", "app", "static", "diagram");
  mkdirSync(staticDir, { recursive: true });
  writeFileSync(join(staticDir, fileName), outHtml);
  console.log(`Wrote ${join(staticDir, fileName)}`);
}

build("dark");
build("light");
