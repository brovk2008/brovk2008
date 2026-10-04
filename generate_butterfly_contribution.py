import urllib.request
import re
from datetime import datetime, date, timedelta

def generate_butterfly_grid():
    now = datetime.now()
    current_year = now.year

    url = f"https://github.com/users/brovk2008/contributions?from={current_year}-01-01&to={current_year}-12-31"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    html = ""
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
    except Exception as e:
        print(f"Failed to fetch from GitHub for {current_year}:", e)
        return

    # Extract total contribution count for current year
    total_contribs_match = re.search(r'([0-9,]+)\s+contributions', html, re.I)
    total_contribs_str = total_contribs_match.group(1) if total_contribs_match else "1,345"

    # Extract all data-date and data-level
    pattern = re.compile(r'<td[^>]*data-date="([^"]+)"[^>]*data-level="([^"]+)"')
    matches = pattern.findall(html)
    date_to_level = {m[0]: int(m[1]) for m in matches}
    
    if not date_to_level:
        print("No contribution dates parsed!")
        return

    # Set up full calendar year for current_year: Jan 1 to Dec 31
    jan1 = date(current_year, 1, 1)
    dec31 = date(current_year, 12, 31)

    # First Sunday on or before Jan 1
    days_back = (jan1.weekday() + 1) % 7 # Sunday = 0, Monday = 1 ... Saturday = 6
    start_sunday = jan1 - timedelta(days=days_back)

    # Map each day of the year into week index and day of week
    weeks = {}
    d = jan1
    while d <= dec31:
        w_day = (d.weekday() + 1) % 7
        w_idx = (d - start_sunday).days // 7
        d_str = d.strftime("%Y-%m-%d")
        lvl = date_to_level.get(d_str, 0)
        if w_idx not in weeks:
            weeks[w_idx] = {}
        weeks[w_idx][w_day] = {"date": d, "level": lvl, "date_str": d_str}
        d += timedelta(days=1)

    num_weeks = max(weeks.keys()) + 1 # 53 weeks (0 to 52)

    # Calculate X positions with clean gaps between months
    col_x_positions = {}
    current_x = 55.0
    cell_step = 13.6
    month_gap = 10.0 # Clear gap between months

    month_ranges = {} # month_num: [x_start, x_end, month_name]
    last_month = None

    for w in range(num_weeks):
        # Determine dominant month in this week
        week_days = weeks.get(w, {})
        # Find which month is present in this week
        primary_date = week_days.get(3, week_days.get(0, None))
        if primary_date:
            m_num = primary_date["date"].month
            m_name = primary_date["date"].strftime("%b")
            
            if last_month is not None and m_num != last_month:
                current_x += month_gap # Add monthly gap!
                
            if m_num not in month_ranges:
                month_ranges[m_num] = [current_x, current_x, m_name]
            else:
                month_ranges[m_num][1] = current_x # update end x
                
            last_month = m_num

        col_x_positions[w] = current_x
        current_x += cell_step

    total_grid_width = current_x + 20
    svg_width = max(960, int(total_grid_width + 40))
    svg_height = 230
    start_y = 66.0
    row_step = 13.6

    active_count = sum(1 for lvl in date_to_level.values() if lvl > 0)

    # Build SVG
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%">')
    svg.append('  <defs>')
    
    # Gradients
    svg.append('    <radialGradient id="bgGrid" cx="50%" cy="50%" r="65%">')
    svg.append('      <stop offset="0%" stop-color="#0c162e"/>')
    svg.append('      <stop offset="60%" stop-color="#070c1b"/>')
    svg.append('      <stop offset="100%" stop-color="#03050c"/>')
    svg.append('    </radialGradient>')

    svg.append('    <radialGradient id="cyanAura" cx="50%" cy="50%" r="50%">')
    svg.append('      <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>')
    svg.append('      <stop offset="35%" stop-color="#7dd3fc" stop-opacity="0.85"/>')
    svg.append('      <stop offset="70%" stop-color="#38bdf8" stop-opacity="0.35"/>')
    svg.append('      <stop offset="100%" stop-color="#38bdf8" stop-opacity="0"/>')
    svg.append('    </radialGradient>')

    svg.append('    <linearGradient id="crystalL1" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('      <stop offset="0%" stop-color="#38bdf8"/>')
    svg.append('      <stop offset="100%" stop-color="#0284c7"/>')
    svg.append('    </linearGradient>')

    svg.append('    <linearGradient id="crystalL2" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('      <stop offset="0%" stop-color="#7dd3fc"/>')
    svg.append('      <stop offset="100%" stop-color="#0ea5e9"/>')
    svg.append('    </linearGradient>')

    svg.append('    <linearGradient id="crystalL3" x1="0%" y1="0%" x2="100%" y2="100%">')
    svg.append('      <stop offset="0%" stop-color="#c084fc"/>')
    svg.append('      <stop offset="100%" stop-color="#6366f1"/>')
    svg.append('    </linearGradient>')

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

    # Filters
    svg.append('    <filter id="softGlow" x="-50%" y="-50%" width="200%" height="200%">')
    svg.append('      <feGaussianBlur stdDeviation="2.2" result="b"/>')
    svg.append('      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>')
    svg.append('    </filter>')

    svg.append('    <filter id="peakGlow" x="-80%" y="-80%" width="260%" height="260%">')
    svg.append('      <feGaussianBlur stdDeviation="4.5" result="b1"/>')
    svg.append('      <feGaussianBlur stdDeviation="1.5" result="b2"/>')
    svg.append('      <feMerge><feMergeNode in="b1"/><feMergeNode in="b2"/><feMergeNode in="SourceGraphic"/></feMerge>')
    svg.append('    </filter>')

    # Butterfly Symbol
    svg.append('    <g id="gridButterfly">')
    svg.append('      <circle cx="0" cy="0" r="13" fill="url(#cyanAura)" opacity="0.85"/>')
    svg.append('      <ellipse cx="0" cy="0" rx="1.3" ry="5.5" fill="#e0f2fe" filter="url(#softGlow)"/>')
    svg.append('      <circle cx="0" cy="-5.5" r="1.3" fill="#ffffff"/>')
    svg.append('      <g>')
    svg.append('        <animateTransform attributeName="transform" type="scale" values="1 1; 0.18 1; 1 1" dur="0.22s" repeatCount="indefinite" additive="sum"/>')
    svg.append('        <path d="M-1,-2 C-8,-11 -15,-7 -14,1 C-13,7 -5,8 -1,3 Z" fill="url(#wingCyan)" opacity="0.9"/>')
    svg.append('        <path d="M-1,2 C-7,6 -10,12 -8,14 C-5,16 -2,12 -1,5 Z" fill="url(#wingViolet)" opacity="0.8"/>')
    svg.append('        <path d="M1,-2 C8,-11 15,-7 14,1 C13,7 5,8 1,3 Z" fill="url(#wingCyan)" opacity="0.9"/>')
    svg.append('        <path d="M1,2 C7,6 10,12 8,14 C5,16 2,12 1,5 Z" fill="url(#wingViolet)" opacity="0.8"/>')
    svg.append('      </g>')
    svg.append('      <path d="M-0.5,-5 C-2,-9 -5,-10 -6,-9" fill="none" stroke="#7dd3fc" stroke-width="0.7"/>')
    svg.append('      <path d="M0.5,-5 C2,-9 5,-10 6,-9" fill="none" stroke="#7dd3fc" stroke-width="0.7"/>')
    svg.append('    </g>')

    # CSS styles
    svg.append('    <style>')
    svg.append('      .mono { font-family: "JetBrains Mono", Consolas, monospace; }')
    svg.append('      .grid-title { font-size: 11px; font-weight: 700; fill: #e0f2fe; letter-spacing: 2px; }')
    svg.append('      .grid-sub { font-size: 8.5px; font-weight: 500; fill: #7dd3fc; letter-spacing: 1px; }')
    svg.append('      .axis-label { font-size: 8px; font-weight: 600; fill: #64748b; }')
    svg.append('      .month-label { font-size: 9px; font-weight: 600; fill: #94a3b8; }')
    svg.append('      .legend-text { font-size: 8px; font-weight: 600; fill: #7dd3fc; }')
    svg.append('    </style>')
    svg.append('  </defs>')

    # Background Box
    svg.append(f'  <rect width="{svg_width}" height="{svg_height}" rx="12" fill="url(#bgGrid)"/>')
    svg.append(f'  <rect width="{svg_width - 2}" height="{svg_height - 2}" x="1" y="1" rx="11" fill="none" stroke="#1e293b" stroke-width="1.2"/>')
    svg.append(f'  <rect width="{svg_width - 8}" height="{svg_height - 8}" x="4" y="4" rx="9" fill="none" stroke="#38bdf8" stroke-width="0.6" stroke-opacity="0.25" stroke-dasharray="8,6"/>')

    # Header with Real Data stats for current year
    svg.append('  <g transform="translate(55, 27)">')
    svg.append(f'    <text y="0" class="mono grid-title" filter="url(#softGlow)">✦ {current_year} CELESTIAL CONTRIBUTION ARCHIVES · {total_contribs_str.upper()} CONTRIBUTIONS ✦</text>')
    svg.append(f'    <text y="14" class="mono grid-sub">{active_count} active starlight days in {current_year} · Full calendar year from Jan to Dec with monthly clustering</text>')
    svg.append('  </g>')

    # Month Labels with centered positions over each month's columns
    for m_num in sorted(month_ranges.keys()):
        x_start, x_end, m_name = month_ranges[m_num]
        center_x = (x_start + x_end) / 2.0
        svg.append(f'  <text x="{center_x:.1f}" y="56" class="mono month-label" text-anchor="middle">{m_name}</text>')

    # Day of week labels (Mon, Wed, Fri)
    days_labels = [("Mon", 1), ("Wed", 3), ("Fri", 5)]
    for dname, didx in days_labels:
        dy = start_y + (didx * row_step) + 3.5
        svg.append(f'  <text x="32" y="{dy:.1f}" class="mono axis-label">{dname}</text>')

    # Crystal Cells by real calendar week and day
    active_waypoints = []
    
    for w in range(num_weeks):
        cx = col_x_positions[w]
        week_days = weeks.get(w, {})
        for day_idx in range(7):
            cy = start_y + (day_idx * row_step)
            
            if day_idx in week_days:
                item = week_days[day_idx]
                lvl = item["level"]
                
                if lvl > 0:
                    active_waypoints.append((cx, cy, lvl, item["date_str"]))

                if lvl == 0:
                    poly = f'<polygon points="{cx:.1f},{cy-4.2:.1f} {cx+4.2:.1f},{cy:.1f} {cx:.1f},{cy+4.2:.1f} {cx-4.2:.1f},{cy:.1f}" fill="#0b1324" stroke="#16233b" stroke-width="0.8"/>'
                elif lvl == 1:
                    poly = f'<polygon points="{cx:.1f},{cy-4.8:.1f} {cx+4.8:.1f},{cy:.1f} {cx:.1f},{cy+4.8:.1f} {cx-4.8:.1f},{cy:.1f}" fill="url(#crystalL1)" stroke="#38bdf8" stroke-width="0.9"/>'
                elif lvl == 2:
                    poly = f'<polygon points="{cx:.1f},{cy-5.2:.1f} {cx+5.2:.1f},{cy:.1f} {cx:.1f},{cy+5.2:.1f} {cx-5.2:.1f},{cy:.1f}" fill="url(#crystalL2)" stroke="#7dd3fc" stroke-width="1.0" filter="url(#softGlow)"/>'
                elif lvl == 3:
                    poly = f'<polygon points="{cx:.1f},{cy-5.6:.1f} {cx+5.6:.1f},{cy:.1f} {cx:.1f},{cy+5.6:.1f} {cx-5.6:.1f},{cy:.1f}" fill="url(#crystalL3)" stroke="#c084fc" stroke-width="1.1" filter="url(#softGlow)"/>'
                else: # lvl >= 4
                    poly = (f'<polygon points="{cx:.1f},{cy-6.2:.1f} {cx+6.2:.1f},{cy:.1f} {cx:.1f},{cy+6.2:.1f} {cx-6.2:.1f},{cy:.1f}" fill="#ffffff" stroke="#38bdf8" stroke-width="1.2" filter="url(#peakGlow)"/>'
                            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.3" fill="#38bdf8"/>')
                
                svg.append(f'  {poly}')

    # Generate smooth butterfly flight trajectory across real active days in current_year
    if len(active_waypoints) >= 12:
        step = len(active_waypoints) // 12
        flight_points = [active_waypoints[i * step] for i in range(12)]
    elif active_waypoints:
        flight_points = active_waypoints
    else:
        flight_points = [(100, 80, 1, ""), (300, 120, 1, ""), (500, 90, 1, ""), (700, 130, 1, "")]

    path_segs = [f"M {flight_points[0][0] - 20:.1f},{flight_points[0][1] + 15:.1f}"]
    for i, pt in enumerate(flight_points):
        px, py = pt[0], pt[1]
        c1x = px - 15
        c1y = py + (12 if i % 2 == 0 else -12)
        path_segs.append(f"C {c1x:.1f},{c1y:.1f} {px - 8:.1f},{py:.1f} {px:.1f},{py:.1f}")
    
    # Return loop
    path_segs.append(f"C {svg_width - 40:.1f},180 {svg_width - 20:.1f},210 {svg_width + 30:.1f},210")
    flight_path_str = " ".join(path_segs)

    svg.append(f'  <path id="butterflyTrack" d="{flight_path_str}" fill="none" stroke="none"/>')

    # Butterfly following trajectory
    svg.append('  <g>')
    svg.append('    <animateMotion dur="20s" repeatCount="indefinite" rotate="auto">')
    svg.append('      <mpath href="#butterflyTrack"/>')
    svg.append('    </animateMotion>')
    svg.append('    <use href="#gridButterfly"/>')
    svg.append('  </g>')

    # Stardust trailing particles
    svg.append('  <g opacity="0.8">')
    svg.append('    <animateMotion dur="20s" repeatCount="indefinite" rotate="auto" begin="-0.25s">')
    svg.append('      <mpath href="#butterflyTrack"/>')
    svg.append('    </animateMotion>')
    svg.append('    <circle cx="-10" cy="1" r="1.5" fill="#38bdf8" filter="url(#softGlow)"/>')
    svg.append('    <circle cx="-16" cy="-2" r="1.0" fill="#c084fc"/>')
    svg.append('    <circle cx="-22" cy="1" r="0.7" fill="#ffffff"/>')
    svg.append('  </g>')

    # Bottom Legend
    leg_x = svg_width - 195
    leg_y = 196
    svg.append('  <g>')
    svg.append(f'    <text x="55" y="198" class="mono legend-text">🦋 SHOREKEEPER BUTTERFLY · {current_year} REAL-TIME ARCHIVES</text>')
    svg.append(f'    <text x="{leg_x - 30}" y="198" class="mono axis-label">Less</text>')
    svg.append(f'    <polygon points="{leg_x},{leg_y-4} {leg_x+4},{leg_y} {leg_x},{leg_y+4} {leg_x-4},{leg_y}" fill="#0b1324" stroke="#16233b" stroke-width="0.8"/>')
    svg.append(f'    <polygon points="{leg_x+14},{leg_y-4.5} {leg_x+18.5},{leg_y} {leg_x+14},{leg_y+4.5} {leg_x+9.5},{leg_y}" fill="url(#crystalL1)" stroke="#38bdf8" stroke-width="0.9"/>')
    svg.append(f'    <polygon points="{leg_x+28},{leg_y-5} {leg_x+33},{leg_y} {leg_x+28},{leg_y+5} {leg_x+23},{leg_y}" fill="url(#crystalL2)" stroke="#7dd3fc" stroke-width="1.0"/>')
    svg.append(f'    <polygon points="{leg_x+42},{leg_y-5.5} {leg_x+47.5},{leg_y} {leg_x+42},{leg_y+5.5} {leg_x+36.5},{leg_y}" fill="url(#crystalL3)" stroke="#c084fc" stroke-width="1.1"/>')
    svg.append(f'    <polygon points="{leg_x+56},{leg_y-6} {leg_x+62},{leg_y} {leg_x+56},{leg_y+6} {leg_x+50},{leg_y}" fill="#ffffff" stroke="#38bdf8" stroke-width="1.2" filter="url(#softGlow)"/>')
    svg.append(f'    <text x="{leg_x + 68}" y="198" class="mono axis-label">More</text>')
    svg.append('  </g>')

    svg.append('</svg>')

    content = "\n".join(svg)
    out_path = r'c:\Users\techp\Downloads\more projects\Github profile\brovk2008\assets\contribution-crystals.svg'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Generated {out_path} ({len(content)} bytes) for full year {current_year}!")

if __name__ == '__main__':
    generate_butterfly_grid()
