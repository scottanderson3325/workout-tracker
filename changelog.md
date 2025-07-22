## [2025-07-22] Initial Schedule & View Workout Routing

### Added
- Flask app routing for:
  - `/` Home page
  - `/schedule` to create and view workouts by week
  - `/view/<int:workout_id>` to view a specific workout
- Logic to repeat workouts weekly for a given number of weeks
- Logic to display workouts by day of week in the schedule view
- SQLAlchemy integration with SQLite database (`workouts.db`)
- Auto-creation of database tables using `db.create_all()` within app context

### Notes
- Repeating logic is controlled by `repeat_weekly` and `repeat_weeks` form fields.
- Navigation between weeks is handled via a `week_offset` query parameter.

### Status
✅ Completed

### Related Files
- `app.py`


## [2025-07-21] Database Model: Workout

### Added
- Defined SQLAlchemy `Workout` model in `models.py` with the following fields:
  - `id`: Primary key
  - `name`: Name of the workout
  - `date`: Date the workout is scheduled
  - `day_of_week`: Text representation of the weekday
  - `repeat_weekly`: Boolean flag for recurring workouts
  - `date_created`: Timestamp of creation (UTC)

### Notes
- The model uses Flask-SQLAlchemy for ORM integration.
- `date_created` uses `datetime.now(timezone.utc)` to store UTC timestamps.

### Status
✅ Completed

### Related Files
- `models.py`


## [2025-07-21] Utility Script: View Saved Workouts

### Added
- `view_db.py` for listing all saved workouts in the database.
- Uses Flask app context to safely query `Workout` model.
- Prints formatted list of saved workouts or indicates if none are found.

### Status
✅ Completed

### Related Files
- `view_db.py`


## [2025-07-21] Utility Script: Clear All Workouts

### Added
- `clear_db.py` for deleting all entries from the `Workout` table.
- Uses Flask app context and `Workout.query.delete()`.
- Confirms deletion by printing number of deleted entries.

### Status
✅ Completed

### Related Files
- `clear_db.py`


## [2025-07-21] Home Page Template

### Added
- `home.html` template for Workout Tracker homepage.
- Integrated Bootstrap 5.3 via CDN for responsive layout and UI styling.
- Included `<meta name="viewport">` for mobile responsiveness.
- Linked to custom stylesheet `style.css` via Flask's `url_for`.
- Homepage contains:
  - Title and subtitle
  - Large button linking to the schedule planner

### Status
✅ Completed

### Related Files
- `templates/home.html`
- `static/style.css`


## [2025-07-21] Weekly Schedule Page Template

### Added
- `schedule.html` template to create and view weekly workouts.
- Features:
  - Workout creation form with support for repeating weekly.
  - Dynamic dropdown to choose number of weeks to repeat (1–10).
  - Week-to-week navigation using "Previous Week" and "Next Week" buttons.
  - Responsive table layout showing workouts per weekday.
  - Integration with `view_workout` route for linking to specific workouts.

### Frontend Enhancements
- Bootstrap 5.3 styling for responsive UI.
- JavaScript to dynamically show/hide repeat week selector based on checkbox state.
- Custom styling with `style.css`.

### Status
✅ Completed

### Related Files
- `templates/schedule.html`
- `static/style.css`


## [2025-07-21] Workout Detail Page Template

### Added
- `view_workout.html` template to display individual workout details.
- Features:
  - Styled card showing workout name, date (formatted), and repeat status.
  - Clear "Back to Schedule" button.
  - Informational alert for debugging: confirms live version is rendering.

### Frontend Enhancements
- Bootstrap 5.3 used for layout and styling.

### Status
✅ Completed

### Related Files
- `templates/view_workout.html`


## [2025-07-21] Custom Stylesheet for Theming

### Added
- `style.css` to customize appearance of UI components.
- Applied styles:
  - Global font and background color
  - Custom color and size for headings and lead text
  - Rounded corners for primary and success buttons
  - Input field and label enhancements for cleaner form appearance

### Notes
- Designed to enhance and complement Bootstrap 5.3 defaults.
- Linked in `home.html`, `schedule.html`, and other templates via `url_for('static', filename='style.css')`.

### Status
✅ Completed

### Related Files
- `static/style.css`


## [2025-07-21] GitHub Project: Completed Issues Sync

### Completed GitHub Issues

1. **Add "Repeat Weekly" Option to Workout Creation**  
   - Implemented boolean flag `repeat_weekly` in form and model.
   - Added repeat loop logic in `/schedule` route.

2. **Set up SQLAlchemy in Flask app**  
   - Integrated SQLAlchemy and configured SQLite database URI.
   - Initialized `db` and created models using `db.create_all()`.

3. **Add Bootstrap to Make App Mobile-Responsive**  
   - Added Bootstrap 5.3 via CDN to all HTML templates.
   - Ensured all UI elements are styled responsively.

4. **Update Workout Model to Include `date` and `day_of_week`**  
   - Expanded `Workout` model with new fields.
   - Extracted day of week from submitted date.

5. **Add Date Picker to Workout Form**  
   - Used HTML5 `<input type="date">` for user-friendly date selection.

6. **Refactor `/schedule` Route to Use Date and Calculate Day**  
   - Extracted date string into Python `datetime`.
   - Derived weekday name programmatically.

7. **Query and Display the Current Week of Workouts**  
   - Queried `Workout` table for all entries within the current week.
   - Used `week_offset` to support navigation.

8. **Render Weekly Schedule as a Table**  
   - Grouped workouts by weekday in a Bootstrap table.
   - Styled table for better visibility and interaction.

9. **Add the ability to scroll to next week to see upcoming workouts**  
   - Implemented week offset logic with buttons to go forward/backward by week.

### Status
✅ All issues above marked **Done** in GitHub.

### Source
- Screenshot reference: `Screenshot 2025-07-21 at 9.20.26 PM.png`



## [2025-07-21] UI Validation: Screenshots of Functional Pages

### Verified Screens
- **Homepage (`home.html`)**
  - Title and subtitle render correctly.
  - Responsive button links to weekly schedule.
  - Styling matches `style.css` and Bootstrap expectations.

- **Schedule Page (`schedule.html`)**
  - Workout creation form includes name, date, repeat options.
  - Workouts display in a table by weekday.
  - Week navigation buttons function visually.
  - Visual confirmation of scheduled workouts: "Leg Day", "Upper Body", "Long Run".

- **Workout Detail View (`view_workout.html`)**
  - Workout details rendered clearly with styled card.
  - Date formatting and repeat status work correctly.
  - Debug banner confirms this is the correct live version of the template.

### Notes
- These screenshots visually confirm full frontend + backend integration.
- Layouts are mobile-friendly and adhere to project style guide.

### Status
✅ Confirmed Functioning (via UI)

### Source
- Screenshot references:
  - `Screenshot 2025-07-21 at 9.21.18 PM.png` (Home)
  - `Screenshot 2025-07-21 at 9.21.27 PM.png` (Schedule)
  - `Screenshot 2025-07-21 at 9.21.35 PM.png` (Workout View)

