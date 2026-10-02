import math
import os

def generate_svg():
    width = 1000
    height = 560
    total_dur = 26 # seconds

    nodes = [
        {"id": "n0", "icon": "🌱", "title": "Genesis", "sub": "I knew nothing · 2020", "x": 75, "y": 120, "era": "ERA 1: GENESIS", "t": 0.0},
        {"id": "n1", "icon": "🖥️", "title": "First Contact", "sub": "Computers &amp; Internet", "x": 215, "y": 85, "era": "ERA 1: CURIOSITY", "t": 2.0},
        {"id": "n2", "icon": "🐍", "title": "Python &amp; Logic", "sub": "First real code · Scripting", "x": 375, "y": 125, "era": "ERA 2: BUILDER", "t": 4.0},
        {"id": "n3", "icon": "🐙", "title": "GitHub", "sub": "Git · Open Repositories", "x": 535, "y": 85, "era": "ERA 2: OPEN SOURCE", "t": 6.0},
        {"id": "n4", "icon": "🤖", "title": "AI &amp; Deep Learning", "sub": "Transformers · LoRA · Ollama", "x": 695, "y": 125, "era": "ERA 3: AI RABBIT HOLE", "t": 8.0},
        {"id": "n5", "icon": "🔌", "title": "Hardware Shift", "sub": "ESP32 · Sensors · Actuators", "x": 870, "y": 95, "era": "ERA 4: EMBEDDED", "t": 10.0},
        {"id": "n6", "icon": "🦾", "title": "Robotics &amp; Actuation", "sub": "Kinematics · ROS2 · Motor loops", "x": 930, "y": 245, "era": "ERA 4: ROBOTICS", "t": 12.0},
        {"id": "n7", "icon": "⚡", "title": "PCB &amp; Circuit Design", "sub": "KiCad schematics · Custom boards", "x": 760, "y": 270, "era": "ERA 4: HARDWARE", "t": 14.0},
        {"id": "n8", "icon": "👓", "title": "Smart Goggles", "sub": "AI + Computer Vision + HW", "x": 580, "y": 240, "era": "ERA 5: CONVERGENCE", "t": 16.0},
        {"id": "n9", "icon": "🏆", "title": "Hackathon Arena", "sub": "46 Built · 14 Wins", "x": 400, "y": 280, "era": "ERA 6: RAPID BUILDS", "t": 18.0},
        {"id": "n10", "icon": "☁️", "title": "Cloud &amp; Infrastructure", "sub": "Docker · AWS · Catalyst · PostGIS", "x": 220, "y": 250, "era": "ERA 7: PRODUCTION", "t": 20.0},
        {"id": "n11", "icon": "📦", "title": "Developer Tools", "sub": "KiCad MCP &amp; DABOOK on PyPI", "x": 85, "y": 320, "era": "ERA 8: DEV TOOLS", "t": 22.0},
        {"id": "n12", "icon": "🌌", "title": "MECH &amp; Beyond", "sub": "Autonomous Systems · 2026", "x": 500, "y": 465, "era": "PRESENT: STILL BUILDING", "t": 24.0},
    ]

    path_d = (
        "M 75,120 "
        "C 135,95 165,85 215,85 "
        "C 275,85 320,125 375,125 "
        "C 435,125 480,85 535,85 "
        "C 595,85 640,125 695,125 "
        "C 765,125 815,95 870,95 "
        "C 915,95 950,175 930,245 "
        "C 890,300 820,270 760,270 "
        "C 690,270 640,240 580,240 "
        "C 510,240 460,280 400,280 "
        "C 330,280 270,250 220,250 "
        "C 160,250 115,270 85,320 "
        "C 50,385 140,465 290,470 "
        "C 380,475 440,468 500,465 "
        "C 580,460 760,490 1020,510"
    )

    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560" width="100%" height="100%">')
    svg.append('  <defs>')
    
    # Gradients
    svg.append('    <radialGradient id="spaceBg" cx="50%" cy="40%" r="65%">')
    svg.append('      <stop offset="0%" stop-color="#0e172e"/>')
    svg.append('      <stop offset="35%" stop-color="#091024"/>')
    svg.append('      <stop offset="70%" stop-color="#050914"/>')
    svg.append('      <stop offset="100%" stop-color="#020409"/>')
    svg.append('    </radialGradient>')

    svg.append('    <radialGradient id="nebulaCyan" cx="30%" cy="25%" r="45%">')
    svg.append('      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.14"/>')
    svg.append('      <stop offset="60%" stop-color="#1e3a8a" stop-opacity="0.05"/>')
    svg.append('      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>')
    svg.append('    </radialGradient>')

    svg.append('    <radialGradient id="nebulaLavender" cx="70%" cy="65%" r="40%">')
    svg.append('      <stop offset="0%" stop-color="#c084fc" stop-opacity="0.12"/>')
    svg.append('      <stop offset="70%" stop-color="#3b0764" stop-opacity="0.04"/>')
    svg.append('      <stop offset="100%" stop-color="#000000" stop-opacity="0"/>')
    svg.append('    </radialGradient>')

    svg.append('    <radialGradient id="coreAura" cx="50%" cy="50%" r="50%">')
    svg.append('      <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>')
    svg.append('      <stop offset="30%" stop-color="#7dd3fc" stop-opacity="0.85"/>')
    svg.append('      <stop offset="65%" stop-color="#38bdf8" stop-opacity="0.35"/>')
    svg.append('      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>')
    svg.append('    </radialGradient>')

    svg.append('    <linearGradient id="crystalIce" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('      <stop offset="0%" stop-color="#ffffff"/>')
    svg.append('      <stop offset="45%" stop-color="#93c5fd"/>')
    svg.append('      <stop offset="100%" stop-color="#2563eb"/>')
    svg.append('    </linearGradient>')

    svg.append('    <linearGradient id="crystalLavender" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('      <stop offset="0%" stop-color="#ffffff"/>')
    svg.append('      <stop offset="40%" stop-color="#e879f9"/>')
    svg.append('      <stop offset="100%" stop-color="#7c3aed"/>')
    svg.append('    </linearGradient>')

    svg.append('    <linearGradient id="activeLine" x1="0%" y1="0%" x2="100%" y2="0%">')
    svg.append('      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/>')
    svg.append('      <stop offset="50%" stop-color="#a855f7" stop-opacity="0.9"/>')
    svg.append('      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.8"/>')
    svg.append('    </linearGradient>')

    # Filters
    svg.append('    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">')
    svg.append('      <feGaussianBlur stdDeviation="3.5" result="blur"/>')
    svg.append('      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>')
    svg.append('    </filter>')

    svg.append('    <filter id="hyperGlow" x="-80%" y="-80%" width="260%" height="260%">')
    svg.append('      <feGaussianBlur stdDeviation="7" result="b1"/>')
    svg.append('      <feGaussianBlur stdDeviation="2.5" result="b2"/>')
    svg.append('      <feMerge><feMergeNode in="b1"/><feMergeNode in="b2"/><feMergeNode in="SourceGraphic"/></feMerge>')
    svg.append('    </filter>')

    # Crystal Symbols
    svg.append('    <g id="crystalNode">')
    svg.append('      <path d="M0,-12 L3,-3 L12,0 L3,3 L0,12 L-3,3 L-12,0 L-3,-3 Z" fill="url(#crystalIce)" filter="url(#softGlow)"/>')
    svg.append('      <path d="M0,-12 L2.5,-2.5 L0,0 L-2.5,-2.5 Z" fill="#ffffff" opacity="0.85"/>')
    svg.append('      <path d="M12,0 L2.5,2.5 L0,0 L2.5,-2.5 Z" fill="url(#crystalLavender)" opacity="0.75"/>')
    svg.append('      <circle cx="0" cy="0" r="2" fill="#ffffff"/>')
    svg.append('    </g>')

    svg.append('    <g id="grandNode">')
    svg.append('      <circle cx="0" cy="0" r="28" fill="url(#coreAura)"/>')
    svg.append('      <circle cx="0" cy="0" r="18" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="3,3" opacity="0.8"/>')
    svg.append('      <path d="M0,-22 L6,-6 L22,0 L6,6 L0,22 L-6,6 L-22,0 L-6,-6 Z" fill="url(#crystalIce)" filter="url(#hyperGlow)"/>')
    svg.append('      <path d="M0,-16 L4,-4 L16,0 L4,4 L0,16 L-4,4 L-16,0 L-4,-4 Z" fill="url(#crystalLavender)"/>')
    svg.append('      <circle cx="0" cy="0" r="3.5" fill="#ffffff" filter="url(#softGlow)"/>')
    svg.append('    </g>')

    # Butterfly Symbol
    svg.append('    <g id="travelerButterfly">')
    svg.append('      <!-- Glow Aura -->')
    svg.append('      <circle cx="0" cy="0" r="16" fill="url(#coreAura)" opacity="0.85"/>')
    svg.append('      <!-- Body -->')
    svg.append('      <ellipse cx="0" cy="0" rx="1.5" ry="6" fill="#e0f2fe" filter="url(#softGlow)"/>')
    svg.append('      <circle cx="0" cy="-6" r="1.5" fill="#ffffff"/>')
    svg.append('      <!-- Left Wing with flap animation -->')
    svg.append('      <g id="leftWing">')
    svg.append('        <animateTransform attributeName="transform" type="scale" values="1 1; 0.15 1; 1 1" dur="0.22s" repeatCount="indefinite" additive="sum"/>')
    svg.append('        <path d="M-1,-2 C-9,-12 -16,-8 -15,1 C-14,8 -6,9 -1,4 Z" fill="url(#crystalIce)" opacity="0.85"/>')
    svg.append('        <path d="M-1,3 C-8,7 -12,13 -9,16 C-6,18 -3,14 -1,6 Z" fill="url(#crystalLavender)" opacity="0.75"/>')
    svg.append('        <path d="M-3,-2 C-8,-7 -12,-4 -11,0 Z" fill="#ffffff" opacity="0.6"/>')
    svg.append('      </g>')
    svg.append('      <!-- Right Wing with flap animation -->')
    svg.append('      <g id="rightWing">')
    svg.append('        <animateTransform attributeName="transform" type="scale" values="1 1; 0.15 1; 1 1" dur="0.22s" repeatCount="indefinite" additive="sum"/>')
    svg.append('        <path d="M1,-2 C9,-12 16,-8 15,1 C14,8 6,9 1,4 Z" fill="url(#crystalIce)" opacity="0.85"/>')
    svg.append('        <path d="M1,3 C8,7 12,13 9,16 C6,18 3,14 1,6 Z" fill="url(#crystalLavender)" opacity="0.75"/>')
    svg.append('        <path d="M3,-2 C8,-7 12,-4 11,0 Z" fill="#ffffff" opacity="0.6"/>')
    svg.append('      </g>')
    svg.append('      <!-- Antennae -->')
    svg.append('      <path d="M-0.5,-6 C-3,-10 -6,-11 -7,-10" fill="none" stroke="#e0f2fe" stroke-width="0.8"/>')
    svg.append('      <path d="M0.5,-6 C3,-10 6,-11 7,-10" fill="none" stroke="#e0f2fe" stroke-width="0.8"/>')
    svg.append('    </g>')

    # CSS styles
    svg.append('    <style>')
    svg.append('      .mono { font-family: "JetBrains Mono", Consolas, "Fira Code", monospace; }')
    svg.append('      .constellation-base { fill: none; stroke: #1e3a5f; stroke-width: 1.6; stroke-dasharray: 4,5; opacity: 0.65; }')
    svg.append('      .constellation-energy { fill: none; stroke: url(#activeLine); stroke-width: 2.2; stroke-linecap: round; }')
    svg.append('      .label-era { font-size: 8px; font-weight: 600; fill: #a78bfa; letter-spacing: 1px; }')
    svg.append('      .label-title { font-size: 11px; font-weight: 700; fill: #e0f2fe; }')
    svg.append('      .label-sub { font-size: 8.5px; font-weight: 400; fill: #7dd3fc; opacity: 0.85; }')
    svg.append('      .chip-bg { fill: #070d1d; fill-opacity: 0.82; stroke: #1e293b; stroke-width: 0.8; rx: 6px; }')
    svg.append('    </style>')

    svg.append('  </defs>')

    # Canvas & Starry Background
    svg.append('  <!-- Canvas & Celestial Nebula -->')
    svg.append('  <rect width="1000" height="560" rx="14" fill="url(#spaceBg)"/>')
    svg.append('  <rect width="1000" height="560" fill="url(#nebulaCyan)"/>')
    svg.append('  <rect width="1000" height="560" fill="url(#nebulaLavender)"/>')
    svg.append('  <rect width="998" height="558" x="1" y="1" rx="13" fill="none" stroke="#1e293b" stroke-width="1.2"/>')
    svg.append('  <rect width="990" height="550" x="5" y="5" rx="10" fill="none" stroke="#38bdf8" stroke-width="0.6" stroke-opacity="0.3" stroke-dasharray="10,6"/>')

    # Background ambient starlight particles
    stars = [
        (130, 60, 1.2, "#ffffff"), (280, 140, 1.0, "#7dd3fc"), (440, 65, 0.8, "#ffffff"),
        (620, 75, 1.4, "#c084fc"), (810, 160, 1.0, "#ffffff"), (960, 120, 1.2, "#38bdf8"),
        (650, 310, 0.9, "#ffffff"), (480, 340, 1.3, "#a78bfa"), (320, 330, 0.8, "#ffffff"),
        (150, 420, 1.1, "#7dd3fc"), (740, 400, 1.4, "#ffffff"), (880, 450, 1.2, "#38bdf8"),
        (220, 500, 0.8, "#c084fc"), (60, 200, 1.0, "#ffffff"), (940, 350, 1.1, "#7dd3fc")
    ]
    svg.append('  <!-- Ambient Stars -->')
    svg.append('  <g opacity="0.65">')
    for sx, sy, sr, sc in stars:
        svg.append(f'    <circle cx="{sx}" cy="{sy}" r="{sr}" fill="{sc}"/>')
    svg.append('  </g>')

    # Top Header
    svg.append('  <!-- Header Title -->')
    svg.append('  <g transform="translate(500, 34)" text-anchor="middle">')
    svg.append('    <text y="-6" class="mono" font-size="9px" font-weight="600" fill="#7dd3fc" letter-spacing="3.5px">✦  S H O R E K E E P E R  ·  C E L E S T I A L  R E C O R D S  ✦</text>')
    svg.append('    <text y="16" class="mono" font-size="16px" font-weight="800" fill="#e0f2fe" letter-spacing="3px" filter="url(#softGlow)">THE DEVELOPER CONSTELLATION</text>')
    svg.append('    <line x1="-240" y1="26" x2="240" y2="26" stroke="url(#activeLine)" stroke-width="1.2"/>')
    svg.append('    <circle cx="0" cy="26" r="3" fill="#38bdf8" filter="url(#softGlow)"/>')
    svg.append('    <circle cx="-240" cy="26" r="1.8" fill="#c084fc"/>')
    svg.append('    <circle cx="240" cy="26" r="1.8" fill="#c084fc"/>')
    svg.append('  </g>')

    # Constellation Lines
    svg.append('  <!-- Constellation Trajectory Lines -->')
    svg.append(f'  <path id="constellationGuide" class="constellation-base" d="{path_d}"/>')
    svg.append(f'  <path id="constellationEnergy" class="constellation-energy" d="{path_d}" stroke-dasharray="14,18">')
    svg.append('    <animate attributeName="stroke-dashoffset" values="320; 0" dur="8s" repeatCount="indefinite"/>')
    svg.append('  </path>')

    # Nodes
    svg.append('  <!-- Milestone Nodes -->')
    for n in nodes:
        nid = n["id"]
        x, y = n["x"], n["y"]
        t = n["t"]
        is_grand = (nid == "n12")

        # Label positioning
        if nid in ["n0", "n2", "n4"]:
            lx = x
            ly = y + 26
            text_anchor = "middle"
            chip_x = lx - 75
            chip_y = ly - 2
            chip_w = 150
            chip_h = 36
        elif nid in ["n1", "n3", "n5"]:
            lx = x
            ly = y - 36
            text_anchor = "middle"
            chip_x = lx - 75
            chip_y = ly - 2
            chip_w = 150
            chip_h = 36
        elif nid in ["n6"]:
            lx = x - 22
            ly = y + 24
            text_anchor = "end"
            chip_x = lx - 146
            chip_y = ly - 2
            chip_w = 150
            chip_h = 36
        elif nid in ["n7", "n9"]:
            lx = x
            ly = y + 26
            text_anchor = "middle"
            chip_x = lx - 75
            chip_y = ly - 2
            chip_w = 150
            chip_h = 36
        elif nid in ["n8", "n10"]:
            lx = x
            ly = y - 36
            text_anchor = "middle"
            chip_x = lx - 75
            chip_y = ly - 2
            chip_w = 150
            chip_h = 36
        elif nid in ["n11"]:
            lx = x + 24
            ly = y - 2
            text_anchor = "start"
            chip_x = lx - 4
            chip_y = ly - 2
            chip_w = 155
            chip_h = 36
        elif is_grand:
            lx = x
            ly = y - 48
            text_anchor = "middle"
            chip_x = lx - 110
            chip_y = ly - 2
            chip_w = 220
            chip_h = 38

        svg.append(f'  <!-- Node {nid}: {n["title"]} -->')
        svg.append(f'  <g id="{nid}_group">')
        
        # Label Chip Background
        svg.append(f'    <rect class="chip-bg" x="{chip_x}" y="{chip_y}" width="{chip_w}" height="{chip_h}"/>')
        
        # Label Texts
        svg.append(f'    <text class="mono" x="{lx}" y="{ly + 10}" text-anchor="{text_anchor}">')
        svg.append(f'      <tspan class="label-era">{n["era"]}</tspan>')
        svg.append(f'    </text>')
        svg.append(f'    <text class="mono" x="{lx}" y="{ly + 21}" text-anchor="{text_anchor}">')
        svg.append(f'      <tspan class="label-title">{n["icon"]} {n["title"]}</tspan>')
        svg.append(f'    </text>')
        svg.append(f'    <text class="mono" x="{lx}" y="{ly + 31}" text-anchor="{text_anchor}">')
        svg.append(f'      <tspan class="label-sub">{n["sub"]}</tspan>')
        svg.append(f'    </text>')

        # Crystal Glyph
        if is_grand:
            svg.append(f'    <g transform="translate({x}, {y})">')
            svg.append(f'      <use href="#grandNode"/>')
            # Expanding shockwave pulse
            svg.append(f'      <circle cx="0" cy="0" r="12" fill="none" stroke="#38bdf8" stroke-width="1.8" opacity="0.9">')
            svg.append(f'        <animate attributeName="r" values="12; 45; 12" dur="3.5s" repeatCount="indefinite"/>')
            svg.append(f'        <animate attributeName="opacity" values="0.9; 0; 0.9" dur="3.5s" repeatCount="indefinite"/>')
            svg.append(f'      </circle>')
            svg.append(f'    </g>')
        else:
            svg.append(f'    <g transform="translate({x}, {y})">')
            # Ambient pulse
            svg.append(f'      <circle cx="0" cy="0" r="14" fill="url(#coreAura)" opacity="0.35">')
            svg.append(f'        <animate attributeName="r" values="10; 16; 10" dur="2.4s" begin="{t * 0.15:.1f}s" repeatCount="indefinite"/>')
            svg.append(f'        <animate attributeName="opacity" values="0.2; 0.55; 0.2" dur="2.4s" begin="{t * 0.15:.1f}s" repeatCount="indefinite"/>')
            svg.append(f'      </circle>')
            svg.append(f'      <use href="#crystalNode"/>')
            svg.append(f'    </g>')

        svg.append(f'  </g>')

    # Butterfly Traveler with Path Follower
    svg.append('  <!-- The Luminous Butterfly Traveler (Narrator) -->')
    svg.append('  <g>')
    svg.append(f'    <animateMotion dur="{total_dur}s" repeatCount="indefinite" rotate="auto">')
    svg.append(f'      <mpath href="#constellationGuide"/>')
    svg.append('    </animateMotion>')
    svg.append('    <use href="#travelerButterfly"/>')
    svg.append('  </g>')

    # Stardust trailing particles along path
    svg.append('  <!-- Stardust Tail particles -->')
    svg.append('  <g opacity="0.8">')
    svg.append(f'    <animateMotion dur="{total_dur}s" repeatCount="indefinite" rotate="auto" begin="-0.25s">')
    svg.append(f'      <mpath href="#constellationGuide"/>')
    svg.append('    </animateMotion>')
    svg.append('    <circle cx="-10" cy="2" r="1.6" fill="#38bdf8" filter="url(#softGlow)"/>')
    svg.append('    <circle cx="-18" cy="-3" r="1.0" fill="#c084fc"/>')
    svg.append('    <circle cx="-25" cy="1" r="0.7" fill="#ffffff"/>')
    svg.append('  </g>')

    # Bottom Footer inside SVG
    svg.append('  <!-- Bottom status caption inside SVG -->')
    svg.append('  <g transform="translate(500, 538)" text-anchor="middle">')
    svg.append('    <text class="mono" font-size="9px" fill="#64748b" letter-spacing="1.5px">')
    svg.append('      <tspan fill="#38bdf8">🦋 The Shorekeeper Butterfly</tspan> traces the continuous evolution of code, silicon &amp; embodied intelligence')
    svg.append('    </text>')
    svg.append('  </g>')

    svg.append('</svg>')

    content = "\n".join(svg)
    out_path = r'c:\Users\techp\Downloads\more projects\Github profile\brovk2008\assets\constellation-journey.svg'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {out_path} ({len(content)} bytes)")

if __name__ == '__main__':
    generate_svg()
