document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-dismiss alerts after 5 seconds
    const alertList = document.querySelectorAll('.alert');
    alertList.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add workout exercise dynamic form
    const addExerciseForm = document.getElementById('add-exercise-form');
    if (addExerciseForm) {
        addExerciseForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const exerciseId = document.getElementById('exercise-select').value;
            const exerciseName = document.getElementById('exercise-select').options[document.getElementById('exercise-select').selectedIndex].text;
            const sets = document.getElementById('sets').value;
            const reps = document.getElementById('reps').value;
            const weight = document.getElementById('weight').value;
            const duration = document.getElementById('duration').value;
            
            if (!exerciseId) {
                alert('Please select an exercise');
                return;
            }
            
            // Create new exercise row
            const exerciseList = document.getElementById('exercise-list');
            const exerciseRow = document.createElement('tr');
            exerciseRow.innerHTML = `
                <td>${exerciseName}
                    <input type="hidden" name="exercises[][id]" value="${exerciseId}">
                </td>
                <td>
                    <input type="number" class="form-control form-control-sm" name="exercises[][sets]" value="${sets}" min="0">
                </td>
                <td>
                    <input type="number" class="form-control form-control-sm" name="exercises[][reps]" value="${reps}" min="0">
                </td>
                <td>
                    <input type="number" class="form-control form-control-sm" name="exercises[][weight]" value="${weight}" min="0" step="0.5">
                </td>
                <td>
                    <input type="number" class="form-control form-control-sm" name="exercises[][duration]" value="${duration}" min="0">
                </td>
                <td>
                    <button type="button" class="btn btn-sm btn-danger remove-exercise">
                        <i class="fas fa-times"></i>
                    </button>
                </td>
            `;
            
            exerciseList.appendChild(exerciseRow);
            
            // Clear form inputs
            document.getElementById('exercise-select').value = '';
            document.getElementById('sets').value = '';
            document.getElementById('reps').value = '';
            document.getElementById('weight').value = '';
            document.getElementById('duration').value = '';
            
            // Add event listener to remove button
            exerciseRow.querySelector('.remove-exercise').addEventListener('click', function() {
                exerciseRow.remove();
            });
        });
    }
    
    // Remove exercise button
    const exerciseList = document.getElementById('exercise-list');
    if (exerciseList) {
        exerciseList.addEventListener('click', function(e) {
            if (e.target.classList.contains('remove-exercise') || e.target.parentElement.classList.contains('remove-exercise')) {
                const row = e.target.closest('tr');
                row.remove();
            }
        });
    }
    
    // Initialize date pickers to today's date if empty
    const datePickers = document.querySelectorAll('input[type="date"]');
    datePickers.forEach(function(picker) {
        if (!picker.value) {
            const today = new Date();
            const month = (today.getMonth() + 1).toString().padStart(2, '0');
            const day = today.getDate().toString().padStart(2, '0');
            picker.value = `${today.getFullYear()}-${month}-${day}`;
        }
    });
});
