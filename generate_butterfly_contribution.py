import urllib.request
import re
from datetime import datetime

def generate_butterfly_grid():
    url = 'https://github.com/users/brovk2008/contributions'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    matches = []
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            matches = re.findall(r'data-date="([^"]+)"[^>]*data-level="([^"]+)"', html)
    except Exception as e:
        print("Failed to fetch online:", e)

    # If offline or failed, fallback to synthetic realistic pattern
    if not matches:
        print("Using synthetic fallback data")
        matches = [("2026-01-01", "0")] * 371

    # Organize into 53 weeks x 7 days
    # Take the last 53 * 7 = 371 days
    total_cells = 53 * 7
    if len(matches) < total_cells:
        matches = [("2025-01-01", "0")] * (total_cells - len(matches)) + matches
    else:
        matches = matches[-total_cells:]

    # Grid parameters
    width = 900
    height = 230
    start_x = 65
    start_y = 65
    step_x = 15.2
    step_y = 15.2

    # Month labels calculation
    # Month positions across 53 weeks
    months = ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
    month_indices = [0, 4, 9, 13, 17, 22, 26, 30, 35, 39, 43, 48, 52]

    svg = []
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 230" width="100%" height="100%">')
    svg.append('  <defs>')
    
    # Gradients
    svg.append('    <radialGradient id="bgGrid" cx="50%" cy="50%" r="65%">')
    svg.append('      <stop offset="0%" stop-color="#0d152a"/>')
    svg.append('      <stop offset="60%" stop-color="#070c1b"/>')
    svg.append('      <stop offset="100%" stop-color="#04060e"/>')
    svg.append('    </radialGradient>')

    svg.append('    <radialGradient id="cyanHalo" cx="50%" cy="50%" r="50%">')
    svg.append('      <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>')
    svg.append('      <stop offset="35%" stop-color="#7dd3fc" stop-opacity="0.8"/>')
    svg.append('      <stop offset="70%" stop-color="#38bdf8" stop-opacity="0.3"/>')
    svg.append('      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>')
    svg.append('    </radialGradient>')

    svg.append('    <linearGradient id="wingCyan" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('      <stop offset="0%" stop-color="#ffffff"/>')
    svg.append('      <stop offset="45%" stop-color="#7dd3fc"/>')
    svg.append('      <stop offset="100%" stop-color="#0284c7"/>')
    svg.append('    </linearGradient>')

    svg.append('    <linearGradient id="wingViolet" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('      <stop offset="0%" stop-color="#ffffff"/>')
    svg.append('      <stop offset="45%" stop-color="#e879f9"/>')
    svg.append('      <stop offset="100%" stop-color="#7c3aed"/>')
    svg.append('    </linearGradient>')

    svg.append('    <linearGradient id="accentBorder" x1="0%" y1="0%" x2="100%" y2="0%">')
    svg.append('      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.6"/>')
    svg.append('      <stop offset="50%" stop-color="#c084fc" stop-opacity="0.8"/>')
    svg.append('      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0.6"/>')
    svg.append('    </linearGradient>')

    # Filters
    svg.append('    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">')
    svg.append('      <feGaussianBlur stdDeviation="2.5" result="blur"/>')
    svg.append('      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>')
    svg.append('    </filter>')

    svg.append('    <filter id="peakGlow" x="-80%" y="-80%" width="260%" height="260%">')
    svg.append('      <feGaussianBlur stdDeviation="4.5" result="b1"/>')
    svg.append('      <feMerge><feMergeNode in="b1"/><feMergeNode in="SourceGraphic"/></feMerge>')
    svg.append('    </filter>')

    # Butterfly Symbol
    svg.append('    <g id="gridButterfly">')
    svg.append('      <circle cx="0" cy="0" r="14" fill="url(#cyanHalo)" opacity="0.8"/>')
    svg.append('      <ellipse cx="0" cy="0" rx="1.2" ry="5.5" fill="#e0f2fe" filter="url(#softGlow)"/>')
    svg.append('      <circle cx="0" cy="-5.5" r="1.3" fill="#ffffff"/>')
    # Flapping Wings
    svg.append('      <g>')
    svg.append('        <animateTransform attributeName="transform" type="scale" values="1 1; 0.18 1; 1 1" dur="0.22s" repeatCount="indefinite" additive="sum"/>')
    svg.append('        <path d="M-1,-2 C-8,-11 -15,-7 -14,1 C-13,7 -5,8 -1,3 Z" fill="url(#wingCyan)" opacity="0.9"/>')
    svg.append('        <path d="M-1,2 C-7,6 -10,12 -8,14 C-5,16 -2,12 -1,5 Z" fill="url(#wingViolet)" opacity="0.8"/>')
    svg.append('        <path d="M1,-2 C8,-11 15,-7 14,1 C13,7 5,8 1,3 Z" fill="url(#wingCyan)" opacity="0.9"/>')
    svg.append('        <path d="M1,2 C7,6 10,12 8,14 C5,16 2,12 1,5 Z" fill="url(#wingViolet)" opacity="0.8"/>')
    svg.append('      </g>')
    # Antennae
    svg.append('      <path d="M-0.5,-5 C-2,-9 -5,-10 -6,-9" fill="none" stroke="#7dd3fc" stroke-width="0.7"/>')
    svg.append('      <path d="M0.5,-5 C2,-9 5,-10 6,-9" fill="none" stroke="#7dd3fc" stroke-width="0.7"/>')
    svg.append('    </g>')

    # CSS styles
    svg.append('    <style>')
    svg.append('      .mono { font-family: "JetBrains Mono", Consolas, monospace; }')
    svg.append('      .grid-title { font-size: 11px; font-weight: 700; fill: #e0f2fe; letter-spacing: 2px; }')
    svg.append('      .grid-sub { font-size: 8.5px; font-weight: 500; fill: #7dd3fc; letter-spacing: 1px; }')
    svg.append('      .axis-label { font-size: 8px; font-weight: 500; fill: #64748b; }')
    svg.append('      .legend-text { font-size: 8px; font-weight: 600; fill: #7dd3fc; }')
    svg.append('    </style>')
    svg.append('  </defs>')

    # Background Box
    svg.append('  <!-- Widget Frame -->')
    svg.append('  <rect width="900" height="230" rx="12" fill="url(#bgGrid)"/>')
    svg.append('  <rect width="898" height="228" x="1" y="1" rx="11" fill="none" stroke="#1e293b" stroke-width="1.2"/>')
    svg.append('  <rect width="892" height="222" x="4" y="4" rx="9" fill="none" stroke="#38bdf8" stroke-width="0.6" stroke-opacity="0.25" stroke-dasharray="8,6"/>')

    # Header in SVG
    svg.append('  <!-- Header Title -->')
    svg.append('  <g transform="translate(65, 28)">')
    svg.append('    <text y="0" class="mono grid-title" filter="url(#softGlow)">✦ CELESTIAL CONTRIBUTION GRID · SHOREKEEPER ARCHIVES</text>')
    svg.append('    <text y="14" class="mono grid-sub">Commits, pull requests &amp; autonomous pipelines reflected as starlight crystals</text>')
    svg.append('  </g>')

    # Month Labels
    svg.append('  <!-- Month Headers -->')
    for m_name, m_idx in zip(months, month_indices):
        mx = start_x + (m_idx * step_x)
        svg.append(f'  <text x="{mx:.1f}" y="56" class="mono axis-label">{m_name}</text>')

    # Day Labels
    days = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    svg.append('  <!-- Day Labels -->')
    for d_name, d_idx in days:
        dy = start_y + (d_idx * step_y) + 4
        svg.append(f'  <text x="36" y="{dy:.1f}" class="mono axis-label">{d_name}</text>')

    # Crystal Grid Rendering
    svg.append('  <!-- Crystal Grid Cells -->')
    active_points = []
    
    for idx, (dt, lvl_str) in enumerate(matches):
        col = idx // 7
        row = idx % 7
        if col >= 53:
            break
            
        cx = start_x + (col * step_x) + 4
        cy = start_y + (row * step_y) + 4
        lvl = int(lvl_str)

        if lvl > 0:
            active_points.append((cx, cy, lvl))

        # Faceted Crystal Polygons by Level
        if lvl == 0:
            # Subtle deep slate crystal outline
            poly = f'<polygon points="{cx},{cy-4.5} {cx+4.5},{cy} {cx},{cy+4.5} {cx-4.5},{cy}" fill="#0b1326" stroke="#192847" stroke-width="0.8"/>'
        elif lvl == 1:
            # Soft cyan starlight crystal
            poly = f'<polygon points="{cx},{cy-5} {cx+5},{cy} {cx},{cy+5} {cx-5},{cy}" fill="#0284c7" stroke="#38bdf8" stroke-width="0.9"/>'
        elif lvl == 2:
            # Luminous cyan crystal
            poly = f'<polygon points="{cx},{cy-5.5} {cx+5.5},{cy} {cx},{cy+5.5} {cx-5.5},{cy}" fill="#0ea5e9" stroke="#7dd3fc" stroke-width="1.0" filter="url(#softGlow)"/>'
        elif lvl == 3:
            # Radiant celestial lavender-cyan crystal
            poly = f'<polygon points="{cx},{cy-6} {cx+6},{cy} {cx},{cy+6} {cx-6},{cy}" fill="#818cf8" stroke="#c084fc" stroke-width="1.1" filter="url(#softGlow)"/>'
        else: # lvl >= 4
            # Peak glowing starlight star crystal
            poly = (f'<polygon points="{cx},{cy-6.5} {cx+6.5},{cy} {cx},{cy+6.5} {cx-6.5},{cy}" fill="#ffffff" stroke="#38bdf8" stroke-width="1.2" filter="url(#peakGlow)"/>'
                    f'<circle cx="{cx}" cy="{cy}" r="1.5" fill="#38bdf8"/>')
        
        svg.append(f'  {poly}')

    # Create Butterfly Trajectory Path through active points
    # Pick a subset of 14 points that smoothly guides the butterfly across the whole grid
    key_waypoints = []
    if len(active_points) >= 10:
        step = len(active_points) // 10
        for i in range(10):
            pt = active_points[i * step]
            key_waypoints.append(pt)
    else:
        key_waypoints = [(100, 80), (200, 140), (350, 90), (500, 150), (650, 100), (780, 130), (840, 80)]

    # Make a smooth curving path across the grid
    path_segs = [f"M {start_x - 10},{start_y + 40}"]
    for i, pt in enumerate(key_waypoints):
        px, py = pt[0], pt[1]
        c1x = px - 20
        c1y = py + (15 if i % 2 == 0 else -15)
        path_segs.append(f"C {c1x:.1f},{c1y:.1f} {px - 10:.1f},{py:.1f} {px:.1f},{py:.1f}")
    path_segs.append(f"C {start_x + 53*step_x + 10:.1f},{start_y + 30} {start_x + 53*step_x + 30:.1f},{start_y + 60} {start_x + 53*step_x + 40:.1f},{start_y + 110}")
    butterfly_path = " ".join(path_segs)

    svg.append('  <!-- Butterfly Trajectory Guide -->')
    svg.append(f'  <path id="butterflyGridPath" d="{butterfly_path}" fill="none" stroke="none"/>')

    # Butterfly following path
    svg.append('  <!-- Butterfly Traveler in Contribution Grid -->')
    svg.append('  <g>')
    svg.append('    <animateMotion dur="18s" repeatCount="indefinite" rotate="auto">')
    svg.append('      <mpath href="#butterflyGridPath"/>')
    svg.append('    </animateMotion>')
    svg.append('    <use href="#gridButterfly"/>')
    svg.append('  </g>')

    # Stardust Tail Sparkles
    svg.append('  <!-- Stardust Tail behind butterfly -->')
    svg.append('  <g opacity="0.75">')
    svg.append('    <animateMotion dur="18s" repeatCount="indefinite" rotate="auto" begin="-0.2s">')
    svg.append('      <mpath href="#butterflyGridPath"/>')
    svg.append('    </animateMotion>')
    svg.append('    <circle cx="-10" cy="1" r="1.5" fill="#38bdf8" filter="url(#softGlow)"/>')
    svg.append('    <circle cx="-16" cy="-2" r="1.0" fill="#c084fc"/>')
    svg.append('    <circle cx="-22" cy="1" r="0.7" fill="#ffffff"/>')
    svg.append('  </g>')

    # Bottom Legend
    svg.append('  <!-- Legend Section -->')
    leg_x = 690
    leg_y = 196
    svg.append('  <g transform="translate(0, 0)">')
    svg.append(f'    <text x="{start_x}" y="198" class="mono legend-text">🦋 THE TRAVELER · GATHERING CELESTIAL CRYSTALS</text>')
    
    svg.append(f'    <text x="{leg_x - 30}" y="198" class="mono axis-label">Less</text>')
    # 5 legend crystals
    svg.append(f'    <polygon points="{leg_x},{leg_y-4} {leg_x+4},{leg_y} {leg_x},{leg_y+4} {leg_x-4},{leg_y}" fill="#0b1326" stroke="#192847" stroke-width="0.8"/>')
    svg.append(f'    <polygon points="{leg_x+14},{leg_y-4.5} {leg_x+18.5},{leg_y} {leg_x+14},{leg_y+4.5} {leg_x+9.5},{leg_y}" fill="#0284c7" stroke="#38bdf8" stroke-width="0.9"/>')
    svg.append(f'    <polygon points="{leg_x+28},{leg_y-5} {leg_x+33},{leg_y} {leg_x+28},{leg_y+5} {leg_x+23},{leg_y}" fill="#0ea5e9" stroke="#7dd3fc" stroke-width="1.0"/>')
    svg.append(f'    <polygon points="{leg_x+42},{leg_y-5.5} {leg_x+47.5},{leg_y} {leg_x+42},{leg_y+5.5} {leg_x+36.5},{leg_y}" fill="#818cf8" stroke="#c084fc" stroke-width="1.1"/>')
    svg.append(f'    <polygon points="{leg_x+56},{leg_y-6} {leg_x+62},{leg_y} {leg_x+56},{leg_y+6} {leg_x+50},{leg_y}" fill="#ffffff" stroke="#38bdf8" stroke-width="1.2" filter="url(#softGlow)"/>')
    svg.append(f'    <text x="{leg_x + 68}" y="198" class="mono axis-label">More</text>')
    svg.append('  </g>')

    svg.append('</svg>')

    content = "\n".join(svg)
    out_path = r'c:\Users\techp\Downloads\more projects\Github profile\brovk2008\assets\contribution-crystals.svg'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {out_path} ({len(content)} bytes)")

if __name__ == '__main__':
    generate_butterfly_grid()
