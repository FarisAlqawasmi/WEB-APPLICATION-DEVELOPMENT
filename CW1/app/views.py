from flask import render_template, redirect, url_for, request, flash
from sqlalchemy import func
from app import app, db
from app.models import Assessment
from app.forms import AssessmentForm


# Homepage route - list all assessments
@app.route('/')
def index():
    """Display all assessments that are not marked as deleted."""
    assessments = Assessment.query.filter_by(is_deleted=False).all()
    return render_template('index.html', assessments=assessments)


# Check if an assessment with the same title and module code exists
def assessment_exists(title, module_code, exclude_id=None):
    query = Assessment.query.filter(
        func.lower(Assessment.title) == func.lower(title),
        func.lower(Assessment.module_code) == func.lower(module_code)
    )
    if exclude_id:
        query = query.filter(Assessment.id != exclude_id)
    return query.first() is not None


# Add a new assessment
@app.route('/add', methods=['GET', 'POST'])
def add_assessment():
    """Add a new assessment, checking for duplicates in title and
    module code."""

    form = AssessmentForm()
    if form.validate_on_submit():
        # Use helper function to check for duplicates
        if assessment_exists(form.title.data, form.module_code.data):
            flash(
                "An assessment with this title "
                "and module code already exists. "
                "Please change the title or module code.",
                "warning"
            )
            return render_template('add.html', form=form)

        # Proceed to add assessment if no duplicates are found
        new_assessment = Assessment(
            title=form.title.data,
            module_code=form.module_code.data,
            deadline=form.deadline.data,
            description=form.description.data
        )
        db.session.add(new_assessment)
        db.session.commit()
        flash("Assessment created successfully!", "success")
        return redirect(url_for('index'))

    return render_template('add.html', form=form)


# Edit an existing assessment
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_assessment(id):
    """Edit an assessment, ensuring no duplicate title and module code
    exists within the same module."""

    assessment = Assessment.query.get_or_404(id)
    form = AssessmentForm(obj=assessment)

    if form.validate_on_submit():
        # Use helper function to check for duplicates,
        # excluding current assessment
        if assessment_exists(
            form.title.data,
            form.module_code.data,
            exclude_id=id
        ):
            flash(
                "An assessment with this title and module code already exists."
                " Please change the title or module code.",
                "warning"
            )
            return render_template(
                'edit.html',
                form=form,
                assessment=assessment
            )

        # Update the assessment if no duplicates are found
        assessment.title = form.title.data
        assessment.module_code = form.module_code.data
        assessment.deadline = form.deadline.data
        assessment.description = form.description.data
        assessment.is_completed = form.is_completed.data
        db.session.commit()
        flash("Assessment updated successfully!", "success")
        return redirect(url_for('index'))

    return render_template('edit.html', form=form, assessment=assessment)


# Mark an assessment as completed
@app.route('/complete/<int:id>')
def complete_assessment(id):
    """Mark an assessment as completed."""
    assessment = Assessment.query.get_or_404(id)
    assessment.is_completed = True
    db.session.commit()
    flash("This assessment has been marked as completed.", "success")
    return redirect(url_for('index'))


# View completed assessments
@app.route('/completed')
def view_completed():
    """Display all assessments marked as completed and not deleted."""
    completed_assessments = Assessment.query.filter_by(
        is_completed=True,
        is_deleted=False
    ).all()
    return render_template(
        'completed.html',
        assessments=completed_assessments
    )


# View uncompleted assessments
@app.route('/uncompleted')
def view_uncompleted():
    """Display all assessments that are uncompleted and not deleted."""
    uncompleted_assessments = Assessment.query.filter_by(
        is_completed=False,
        is_deleted=False
    ).all()
    return render_template(
        'uncompleted.html',
        assessments=uncompleted_assessments
    )


# Delete an assessment (soft delete)
@app.route('/delete/<int:id>', methods=['POST'])
def delete_assessment(id):
    """Soft delete an assessment by marking it as deleted."""
    assessment = Assessment.query.get_or_404(id)
    assessment.is_deleted = True
    db.session.commit()
    flash(f"The assessment '{assessment.title}' has been deleted.", "info")

    next_page = request.form.get('next')
    if next_page:
        return redirect(next_page)
    return redirect(url_for('index'))


# View deleted assessments
@app.route('/deleted')
def view_deleted_assessments():
    """Display only deleted assessments."""
    deleted_assessments = Assessment.query.filter_by(is_deleted=True).all()
    return render_template('deleted.html', assessments=deleted_assessments)


# Restore a deleted assessment
@app.route('/restore/<int:id>', methods=['POST'])
def restore_assessment(id):
    """Restore a previously deleted assessment."""
    assessment = Assessment.query.get_or_404(id)
    assessment.is_deleted = False
    db.session.commit()
    flash(f"The assessment '{assessment.title}' has been restored.", "success")
    return redirect(url_for('view_deleted_assessments'))


# Permanently delete an assessment
@app.route('/permanent_delete/<int:id>', methods=['POST'])
def delete_assessment_permanently(id):
    """Permanently delete an assessment from the database."""
    assessment = Assessment.query.get_or_404(id)
    db.session.delete(assessment)
    db.session.commit()
    flash(
        f"The assessment '{assessment.title}' has been permanently deleted.",
        "danger"
    )
    return redirect(url_for('view_deleted_assessments'))
