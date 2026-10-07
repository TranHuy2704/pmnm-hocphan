Python
import csv
import io
from markupsafe import escape
from flask import Flask, request, jsonify, url_for, redirect, abort, make_response

app = Flask(__name__)
app.json.ensure_ascii = False

STUDENTS = {
    "23T1020001": {"name": "Nguyễn Văn An", "lop": "K47A",
                   "scores": {"PMMNM": 8.5, "CSDL": 7.0, "MMT": 9.0}},
    "23T1020002": {"name": "Trần Thị Bình", "lop": "K47A",
                   "scores": {"PMMNM": 6.0, "CSDL": 5.5, "MMT": 7.0}},
    "23T1020003": {"name": "Lê Hoàng Cường", "lop": "K47B",
                   "scores": {"PMMNM": 9.5, "CSDL": 9.0}},
    "23T1020004": {"name": "Phạm Minh Dũng", "lop": "K47B",
                   "scores": {"PMMNM": 4.0, "CSDL": 3.5, "MMT": 5.0}},
    "23T1020005": {"name": "Hoàng Thu Hà", "lop": "K47A",
                   "scores": {}},
    "23T1020006": {"name": "Võ Quốc Khánh", "lop": "K47C",
                   "scores": {"PMMNM": 7.5, "MMT": 8.0}},
}

def average(scores):
    if not scores:
        return None
    vals = list(scores.values())
    return round(sum(vals) / len(vals), 2)

def rank(avg):
    if avg is None:
        return "Chưa có điểm"
    if avg >= 8.5:
        return "Giỏi"
    if avg >= 7.0:
        return "Khá"
    if avg >= 5.0:
        return "Trung bình"
    return "Yếu"

def student_summary(mssv):
    std = STUDENTS.get(mssv)
    if not std:
        return None
    avg = average(std["scores"])
    return {
        "mssv": mssv,
        "name": std["name"],
        "lop": std["lop"],
        "scores": std["scores"],
        "average": avg,
        "rank": rank(avg)
    }

def layout(title, body):
    escaped_title = escape(title)
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>{escaped_title} - Sổ điểm</title>
</head>
<body>
    <nav>
        <a href="{url_for('home')}">Trang chủ</a> | 
        <a href="{url_for('student_list')}">Sinh viên</a> | 
        <a href="{url_for('search')}">Tìm kiếm</a>
    </nav>
    <hr>
    <div>
        {body}
    </div>
</body>
</html>"""

@app.route("/")
def home():
    total_students = len(STUDENTS)
    classes = sorted(list(set(std["lop"] for std in STUDENTS.values())))
    content = f"""
    <h2>Hệ thống quản lý Sổ điểm</h2>
    <p>Tổng số sinh viên: <strong>{total_students}</strong></p>
    <p>Số lớp: <strong>{len(classes)}</strong></p>
    <ul>
        <li><a href="{url_for('student_list')}">Xem danh sách sinh viên</a></li>
        <li><a href="{url_for('api_students')}">API danh sách sinh viên</a></li>
    </ul>
    """
    return layout("Trang chủ", content)

@app.route("/students")
def student_list():
    lop_filter = request.args.get("lop", "").strip()
    classes = sorted(list(set(std["lop"] for std in STUDENTS.values())))
    
    filter_links = [f'<a href="{url_for("student_list")}">Tất cả</a>']
    for c in classes:
        filter_links.append(f'<a href="{url_for("student_list", lop=c)}">{escape(c)}</a>')
    filter_bar = " | ".join(filter_links)
    
    matched = []
    for mssv, data in STUDENTS.items():
        if lop_filter:
            if data["lop"].lower() == lop_filter.lower():
                matched.append(mssv)
        else:
            matched.append(mssv)
            
    if not matched:
        table_html = "<p>Không có sinh viên phù hợp.</p>"
    else:
        rows = []
        for mssv in matched:
            info = student_summary(mssv)
            avg_str = f"{info['average']:.2f}" if info['average'] is not None else "-"
            rows.append(f"""<tr>
                <td><a href="{url_for('student_detail', mssv=mssv)}">{escape(info['mssv'])}</a></td>
                <td>{escape(info['name'])}</td>
                <td>{escape(info['lop'])}</td>
                <td>{escape(avg_str)}</td>
                <td>{escape(info['rank'])}</td>
            </tr>""")
            
        table_html = f"""<table border="1" cellpadding="6" style="border-collapse: collapse;">
            <thead>
                <tr>
                    <th>MSSV</th>
                    <th>Họ tên</th>
                    <th>Lớp</th>
                    <th>Điểm TB</th>
                    <th>Xếp loại</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>"""
        
    content = f"""
    <h2>Danh sách sinh viên</h2>
    <p>Bộ lọc: {filter_bar}</p>
    {table_html}
    """
    return layout("Danh sách sinh viên", content)

@app.route("/students/<mssv>")
def student_detail(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
        
    info = student_summary(mssv)
    avg_display = f"{info['average']:.2f}" if info['average'] is not None else "Chưa có điểm"
    score_rows = [f"<li>{escape(k)}: {escape(str(v))}</li>" for k, v in info["scores"].items()]
    scores_html = f"<ul>{''.join(score_rows)}</ul>" if score_rows else "<p>Chưa có điểm học phần nào.</p>"
    
    content = f"""
    <h2>Chi tiết sinh viên: {escape(info['name'])}</h2>
    <p><strong>MSSV:</strong> {escape(info['mssv'])}</p>
    <p><strong>Lớp:</strong> <a href="{url_for('student_list', lop=info['lop'])}">{escape(info['lop'])}</a></p>
    <p><strong>Điểm TB:</strong> {escape(str(avg_display))}</p>
    <p><strong>Xếp loại:</strong> {escape(info['rank'])}</p>
    <p><strong>Link rút gọn (Câu 4):</strong> <a href="{url_for('short_student_link', mssv=mssv)}">{url_for('short_student_link', mssv=mssv)}</a></p>
    <h3>Bảng điểm chi tiết:</h3>
    {scores_html}
    <p><a href="{url_for('export_csv', mssv=mssv)}">Tải bảng điểm (CSV)</a></p>
    """
    return layout(f"Sinh viên {info['name']}", content)

@app.route("/sv/<mssv>")
def short_student_link(mssv):
    return redirect(url_for("student_detail", mssv=mssv), code=301)

@app.route("/students/<mssv>/export")
def export_csv(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
        
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["hoc_phan", "diem"])
    for k, v in STUDENTS[mssv]["scores"].items():
        writer.writerow([k, v])
        
    res = make_response(output.getvalue())
    res.headers["Content-Type"] = "text/csv; charset=utf-8"
    res.headers["Content-Disposition"] = f"attachment; filename=diem_{mssv}.csv"
    return res

@app.route("/search")
def search():
    q = request.args.get("q", "")
    escaped_q = escape(q)
    results_html = ""
    
    if q != "":
        kw = q.strip().lower()
        matched = [(m, d["name"]) for m, d in STUDENTS.items() if kw in m.lower() or kw in d["name"].lower()]
        results_html += f"<p>Tìm thấy {len(matched)} kết quả cho “{escaped_q}”</p>"
        if matched:
            items = [f'<li><a href="{url_for("student_detail", mssv=m)}">{escape(m)} - {escape(n)}</a></li>' for m, n in matched]
            results_html += f"<ul>{''.join(items)}</ul>"
            
    content = f"""
    <h2>Tìm kiếm sinh viên</h2>
    <form method="GET" action="{url_for('search')}">
        <input type="text" name="q" value="{escaped_q}" placeholder="Nhập tên hoặc MSSV...">
        <button type="submit">Tìm</button>
    </form>
    <div>
        {results_html}
    </div>
    """
    return layout("Tìm kiếm", content)

@app.route("/api/students")
def api_students():
    lop = request.args.get("lop")
    min_avg_raw = request.args.get("min_avg")
    min_avg = None
    
    if min_avg_raw is not None:
        try:
            min_avg = float(min_avg_raw)
        except ValueError:
            abort(400, description="Tham số min_avg phải là số thực.")
            
    res = []
    for mssv in STUDENTS:
        info = student_summary(mssv)
        if lop is not None and info["lop"].lower() != lop.strip().lower():
            continue
        if min_avg is not None and (info["average"] is None or info["average"] < min_avg):
            continue
        res.append(info)
    return jsonify(res)

@app.route("/api/students/<mssv>")
def api_student_single(mssv):
    if mssv not in STUDENTS:
        abort(404, description=f"Không có sinh viên với MSSV = {mssv}.")
    return jsonify(student_summary(mssv))

@app.route("/api/students/<mssv>/scores/<course>", methods=["GET", "PUT", "DELETE"])
def api_student_course_score(mssv, course):
    if mssv not in STUDENTS:
        abort(404, description=f"Không tìm thấy sinh viên với MSSV = {mssv}.")
        
    std = STUDENTS[mssv]
    c_code = course.strip().upper()
    
    if request.method == "GET":
        if c_code not in std["scores"]:
            abort(404, description=f"Học phần {c_code} chưa có điểm.")
        return jsonify({"mssv": mssv, "course": c_code, "score": std["scores"][c_code]}), 200

    elif request.method == "PUT":
        score_val = request.args.get("score")
        if score_val is None:
            abort(400, description="Thiếu tham số 'score'.")
        try:
            score = float(score_val)
        except ValueError:
            abort(400, description="Tham số 'score' phải là số thực.")
            
        if not (0.0 <= score <= 10.0):
            abort(400, description="Điểm số phải nằm trong khoảng [0, 10].")
            
        is_new = c_code not in std["scores"]
        std["scores"][c_code] = score
        new_avg = average(std["scores"])
        
        if is_new:
            return jsonify({"average": new_avg}), 201, {"Location": url_for("api_student_course_score", mssv=mssv, course=c_code)}
        return jsonify({"average": new_avg}), 200

    elif request.method == "DELETE":
        if c_code not in std["scores"]:
            abort(404, description=f"Học phần {c_code} chưa có điểm để xoá.")
        del std["scores"][c_code]
        return "", 204