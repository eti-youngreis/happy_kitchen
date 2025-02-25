import base64
import io
import matplotlib.pyplot as plt
from bidi import algorithm as bidialg
from constants import CourseType, DairyType
from flask import Blueprint, render_template
from services.recipe_service import get_recipes
import matplotlib
matplotlib.use('Agg')


statistics_bp = Blueprint('statistics', __name__)


@statistics_bp.route('/statistics')
def show_statistics():
    graph_url_1 = create_recipe_distribution_graph()
    graph_url_2 = create_cooking_time_distribution_graph()
    return render_template('statistics.html', graph_url_1=graph_url_1, graph_url_2=graph_url_2)


def create_recipe_distribution_graph():
    recipes = get_recipes()
    course_types = CourseType.all()
    dairy_types = DairyType.all()
    data = {course: {dairy: 0 for dairy in dairy_types}
            for course in course_types}

    for recipe in recipes:
        if recipe.course_type in course_types and recipe.dairy_type in dairy_types:
            data[recipe.course_type][recipe.dairy_type] += 1

    _, ax = plt.subplots(figsize=(5, 6))

    x = range(len(course_types))
    width = 0.8 / len(dairy_types)

    for i, dairy in enumerate(dairy_types):
        values = [data[course][dairy] for course in course_types]
        ax.bar([xi + i * width for xi in x], values, width,
               label=bidialg.get_display(dairy))

    ax.set_xlabel(bidialg.get_display(u'סוג מנה'))
    ax.set_ylabel(bidialg.get_display(u'מספר מתכונים'))
    ax.set_title(bidialg.get_display(
        u'התפלגות מתכונים לפי סוג מנה וסוג מתכון'))
    ax.set_xticks([xi + width * (len(dairy_types) - 1) / 2 for xi in x])
    ax.set_xticklabels([bidialg.get_display(course)
                       for course in course_types])
    ax.legend()

    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return graph_url
def create_cooking_time_distribution_graph():
    recipes = get_recipes()
    cooking_times = [recipe.cooking_time for recipe in recipes if recipe.cooking_time is not None]

    time_categories = ['0-15', '16-30', '31-60', '61-90', '91+']
    time_counts = [0] * len(time_categories)

    for time in cooking_times:
        if time <= 15:
            time_counts[0] += 1
        elif time <= 30:
            time_counts[1] += 1
        elif time <= 60:
            time_counts[2] += 1
        elif time <= 90:
            time_counts[3] += 1
        else:
            time_counts[4] += 1

    fig, ax = plt.subplots(figsize=(5, 6))

    ax.bar(time_categories, time_counts)

    ax.set_xlabel(bidialg.get_display(u'זמן הכנה (דקות)'))
    ax.set_ylabel(bidialg.get_display(u'מספר מתכונים'))
    ax.set_title(bidialg.get_display(u'התפלגות מתכונים לפי זמן הכנה'))

    for i, v in enumerate(time_counts):
        ax.text(i, v, str(v), ha='center', va='bottom')

    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return graph_url
