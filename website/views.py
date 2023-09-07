from flask import Blueprint, render_template, request, flash, redirect,url_for
from flask_login import login_required, current_user
from .models import Post, User
from . import db
views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', user=current_user, posts=reversed(posts))

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method=='POST':
        text = request.form.get('text')

        if not text:
            flash('A publicação não pode ser vazia!', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Publicação criada com sucesso!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)

@views.route("delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash('Essa Publicação não existe.', category='error')
    elif current_user.id != post.author:
        flash('Você não tem permissão para deletar essa publicação', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Publicação deletada.', category='success')
    
    return redirect(url_for('views.home'))

@views.route('/posts/<username>')
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('Não existe um usuário com esse nome.',category='error')
        return redirect(url_for('views.home'))
    
    posts = Post.query.filter_by(author=user.id).all()
    return render_template('posts.html', user=current_user, posts=posts, username=username)