from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from services.recipe_service import (
    add_recipe as service_add_recipe,
    delete_recipe as delete_recipe_service,
    get_recipe_by_id,
    get_recipes,
    update_recipe as update_recipe_service,
)

recipe_bp = Blueprint('recipe', __name__)


@recipe_bp.route("/")
def home():
    search_query = request.args.get('query', '')
    dairy_type = request.args.get('dairy_type', '')
    course_type = request.args.get('course_type', '')
    recipes = get_recipes(search_query, dairy_type, course_type)
    return render_template("home.html", recipes=recipes)

@recipe_bp.route("/about")
def about():
    return render_template("about.html")

@recipe_bp.route("/<int:recipe_id>")
def recipe(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    return render_template("recipe.html", recipe=recipe)


@recipe_bp.route("/add-recipe")
@login_required
def add_recipe():
    return render_template("add_recipe.html")


@recipe_bp.route("/submit-recipe", methods=['POST'])
@login_required
def submit_recipe():
    new_recipe = service_add_recipe(
        request.form, request.files['image'], current_user.id)
    if new_recipe:
        flash('המתכון נוסף בהצלחה!', 'success')
        return redirect(url_for('recipe.recipe', recipe_id=new_recipe.id))
    else:
        flash('אירעה שגיאה בהוספת המתכון. אנא נסה שנית.', 'error')
        return redirect(url_for('recipe.add_recipe'))


@recipe_bp.route("/<int:recipe_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        flash('המתכון המבוקש לא נמצא.', 'error')
        return redirect(url_for('recipe.home'))
    if recipe.user_id != current_user.id:
        flash('אין לך הרשאה לערוך מתכון זה.', 'error')
        return redirect(url_for('recipe.home'))

    if request.method == 'POST':
        updated_recipe = update_recipe_service(
            recipe_id, request.form, request.files.get('image'))
        if updated_recipe:
            flash('המתכון עודכן בהצלחה!', 'success')
            return redirect(url_for('recipe.recipe', recipe_id=recipe_id))
        else:
            flash('אירעה שגיאה בעדכון המתכון. אנא נסה שנית.', 'error')

    return render_template("edit_recipe.html", recipe=recipe)


@recipe_bp.route("/<int:recipe_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_recipe(recipe_id):
    recipe = get_recipe_by_id(recipe_id)
    if not recipe:
        flash('המתכון המבוקש לא נמצא.', 'error')
        return redirect(url_for('recipe.home'))
    if recipe.user_id != current_user.id:
        flash('אין לך הרשאה למחוק מתכון זה.', 'error')
        return redirect(url_for('recipe.home'))

    if delete_recipe_service(recipe_id):
        flash('המתכון נמחק בהצלחה!', 'success')
    else:
        flash('אירעה שגיאה במחיקת המתכון. אנא נסה שנית.', 'error')
    return redirect(url_for('recipe.home'))


@recipe_bp.route('/my_recipes')
@login_required
def my_recipes():
    user_recipes = current_user.recipes
    return render_template('home.html', recipes=user_recipes)
