import logging

from flask import Blueprint, render_template, request, redirect, url_for

from app.api.snapchat_api import SnapchatAPI
from app.models.models import Segment, Identifier, IdentifierType

main_blueprint = Blueprint("main", __name__)
app_logger = logging.getLogger("app_logger")


@main_blueprint.route("/")
def dashboard():
    app_logger.info("Fetching all segments from Snapchat API")
    segments = SnapchatAPI.fetch_all_segments()
    app_logger.info(f"Segments fetched: {segments}")
    return render_template("dashboard.html", segments=segments)


@main_blueprint.route("/add_user_to_segment/<int:segment_id>", methods=["GET", "POST"])
def add_user_to_segment(segment_id):
    if request.method == "POST":
        app_logger.info(f"Adding user to segment {segment_id}")
        identifier_type = request.form["identifier_type"]
        identifier_values = request.form.getlist("identifier_value[]")
        existing_identifiers = {
            id.value for id in Identifier.query.filter_by(segment_id=segment_id).all()
        }
        new_identifiers = [
            id_value
            for id_value in identifier_values
            if id_value not in existing_identifiers
        ]
        errors = []
        if len(new_identifiers) < len(identifier_values):
            # Collect duplicates to report
            duplicate_identifiers = set(identifier_values) - set(new_identifiers)
            errors.append(
                f"Identifiers {', '.join(duplicate_identifiers)} already exist in this segment and were not added."
            )
            app_logger.warning(
                f"Duplicate identifiers not added: {duplicate_identifiers}"
            )
        response = SnapchatAPI.add_users_to_segment(
            segment_id, identifier_type, identifier_values
        )
        app_logger.info(f"Response from Snapchat API: {response}")
        if response["request_status"] == "SUCCESS":
            for id_value in new_identifiers:
                identifier_type = IdentifierType.query.filter_by(
                    name=identifier_type
                ).first()
                new_identifier = Identifier(
                    value=id_value, type=identifier_type, segment_id=segment_id
                )
                new_identifier.save()
                app_logger.info(f"New identifier saved: {id_value}")
        if errors:
            # Return to the form with an error
            identifiers = Identifier.query.filter_by(segment_id=segment_id).all()
            return render_template(
                "view_segment_users.html",
                segment=segment_id,
                identifiers=identifiers,
                errors=errors,
            )
        return redirect(url_for("main.view_segment_identifiers", segment_id=segment_id))

    return render_template("add_user_to_segment.html", segment_id=segment_id)


@main_blueprint.route("/add_segment", methods=["GET", "POST"])
def add_segment():
    if request.method == "POST":
        app_logger.info("Attempting to add a new segment")
        segment_name = request.form["name"]
        segment_description = request.form["description"]
        segment_retention_days = request.form["retention_days"]
        existing_segments = SnapchatAPI.fetch_all_segments()
        app_logger.info("Checking for existing segments to avoid duplicates")
        errors = None
        for existing_segment in existing_segments:
            if existing_segment["name"] == segment_name:
                errors = ["Segment with the same name already exists!"]
                app_logger.error("Segment creation failed: Duplicate name")
                break
        if errors:
            # Return to the form with an error
            return render_template("add_segment.html", errors=errors)
        segment = SnapchatAPI.add_new_segment(
            segment_name, segment_description, segment_retention_days
        )
        new_segment = Segment(id=segment["id"], name=segment["name"])
        new_segment.save()
        app_logger.info(f"New segment added: {segment['name']}")
        return redirect(url_for("main.dashboard"))

    return render_template("add_segment.html")


@main_blueprint.route("/update_segment/<int:segment_id>", methods=["GET", "POST"])
def update_segment(segment_id):
    if request.method == "POST":
        app_logger.info(f"Updating segment {segment_id}")
        segment_name = request.form["name"]
        segment_description = request.form["description"]
        segment_retention_days = request.form["retention_days"]
        SnapchatAPI.update_segment(
            segment_id, segment_name, segment_description, segment_retention_days
        )
        segment = Segment.query.get(segment_id)
        if segment:
            name = segment_name
            segment.update(name=name)
            app_logger.info(f"Updated segment {segment_id}")
            return redirect(url_for("main.dashboard"))
        return redirect(url_for("main.dashboard"))
    segment = SnapchatAPI.get_segment(segment_id)
    return render_template("update_segment.html", segment=segment)


@main_blueprint.route("/delete_segment", methods=["POST"])
def delete_segment():
    app_logger.info("Attempting to delete segment")
    segment_id = request.form["segment_id"]
    SnapchatAPI.delete_segment(segment_id)
    segment = Segment.query.get(segment_id)
    if segment:
        segment.delete()
        app_logger.info(f"Deleted Segment {segment_id}")
    return redirect(url_for("main.dashboard"))


@main_blueprint.route("/view_segment_identifiers/<string:segment_id>", methods=["GET"])
def view_segment_identifiers(segment_id):
    app_logger.info(f"Fetching Segment {segment_id} Identifiers")
    identifiers = Identifier.query.filter_by(segment_id=segment_id).all()
    return render_template(
        "view_segment_users.html", segment=segment_id, identifiers=identifiers
    )
