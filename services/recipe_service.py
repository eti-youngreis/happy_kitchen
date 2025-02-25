import os
import time
from typing import List, Optional
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from models.models import Recipe
from extensions import db
from flask import current_app


def get_recipes(search_query: str = '', dairy_type: str = '', course_type: str = '') -> List[Recipe]:
    """
    Retrieve recipes based on search criteria.
    """
    query = Recipe.query
    if search_query:
        query = query.filter(Recipe.name.ilike(f'%{search_query}%'))
    if dairy_type:
        query = query.filter(Recipe.dairy_type == dairy_type)
    if course_type:
        query = query.filter(Recipe.course_type == course_type)
    return query.all()


def get_recipe_by_id(recipe_id: int) -> Optional[Recipe]:
    """
    Retrieve a recipe by its ID.
    """
    return Recipe.query.get(recipe_id)


def add_recipe(form_data: dict, image: FileStorage, user_id: int) -> Optional[Recipe]:
    """
    Add a new recipe to the database.
    """
    try:
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            image_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], unique_filename)

            # Ensure the upload folder exists
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            image.save(image_path)
            relative_image_path = f"/{current_app.config['UPLOAD_FOLDER']}/{unique_filename}"

            new_recipe = Recipe(
                name=form_data['name'],
                ingredients=form_data['ingredients'],
                instructions=form_data['instructions'],
                cooking_time=form_data['cooking_time'],
                difficulty=form_data['difficulty'],
                course_type=form_data['course_type'],
                dairy_type=form_data['dairy_type'],
                image_path=relative_image_path,
                user_id=user_id  # Add this line
            )
            db.session.add(new_recipe)
            db.session.commit()
            return new_recipe
        else:
            current_app.logger.error("Invalid file or no file uploaded")
    except Exception as e:
        current_app.logger.error(f"Error adding recipe: {str(e)}")
        db.session.rollback()
    return None


def allowed_file(filename: str) -> bool:
    """
    Check if the file extension is allowed.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in current_app.config['ALLOWED_EXTENSIONS']


def update_recipe(recipe_id, form_data, image=None):
    try:
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            return None

        recipe.name = form_data['name']
        recipe.ingredients = form_data['ingredients']
        recipe.instructions = form_data['instructions']
        recipe.cooking_time = form_data['cooking_time']
        recipe.difficulty = form_data['difficulty']
        recipe.course_type = form_data['course_type']
        recipe.dairy_type = form_data['dairy_type']

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            unique_filename = f"{int(time.time())}_{filename}"
            image_path = os.path.join(
                current_app.config['UPLOAD_FOLDER'], unique_filename)
            image.save(image_path)
            recipe.image_path = f"/{current_app.config['UPLOAD_FOLDER']}/{unique_filename}"

        db.session.commit()
        return recipe
    except Exception as e:
        current_app.logger.error(f"Error updating recipe: {str(e)}")
        db.session.rollback()
        return None


def delete_recipe(recipe_id):
    try:
        recipe = Recipe.query.get(recipe_id)
        if not recipe:
            current_app.logger.error(f"Recipe with id {recipe_id} not found")
            return False

        if recipe.image_path:
            image_path = os.path.join(
                current_app.root_path, recipe.image_path.lstrip('/'))
            if os.path.exists(image_path):
                os.remove(image_path)

        db.session.delete(recipe)
        db.session.commit()
        current_app.logger.info(
            f"Recipe with id {recipe_id} successfully deleted")
        return True
    except Exception as e:
        current_app.logger.error(f"Error deleting recipe: {str(e)}")
        db.session.rollback()
        return False
