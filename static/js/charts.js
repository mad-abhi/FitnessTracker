document.addEventListener('DOMContentLoaded', function() {
    // Weekly Workout Chart
    const workoutChartElement = document.getElementById('workoutChart');
    if (workoutChartElement) {
        const workoutChart = new Chart(workoutChartElement, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Workouts',
                    data: workoutData || [0, 0, 0, 0, 0, 0, 0],
                    backgroundColor: 'rgba(13, 110, 253, 0.7)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    // Calories Burned Chart
    const caloriesChartElement = document.getElementById('caloriesChart');
    if (caloriesChartElement) {
        const caloriesChart = new Chart(caloriesChartElement, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Calories',
                    data: caloriesData || [0, 0, 0, 0, 0, 0, 0],
                    backgroundColor: 'rgba(40, 167, 69, 0.2)',
                    borderColor: 'rgba(40, 167, 69, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    // Progress Chart for Goals
    const goalChartElements = document.querySelectorAll('.goal-chart');
    goalChartElements.forEach(function(element) {
        const goalId = element.getAttribute('data-goal-id');
        const currentValue = parseFloat(element.getAttribute('data-current-value'));
        const targetValue = parseFloat(element.getAttribute('data-target-value'));
        
        const progress = (currentValue / targetValue) * 100;
        const remaining = 100 - progress;
        
        const goalChart = new Chart(element, {
            type: 'doughnut',
            data: {
                labels: ['Progress', 'Remaining'],
                datasets: [{
                    data: [currentValue, Math.max(0, targetValue - currentValue)],
                    backgroundColor: [
                        'rgba(13, 110, 253, 0.8)',
                        'rgba(233, 236, 239, 1)'
                    ],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '75%',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const value = context.raw;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${context.label}: ${percentage}%`;
                            }
                        }
                    }
                }
            }
        });
        
        // Add center text
        Chart.register({
            id: 'center-text',
            beforeDraw: function(chart) {
                const width = chart.width;
                const height = chart.height;
                const ctx = chart.ctx;
                
                ctx.restore();
                ctx.font = '16px Arial';
                ctx.textBaseline = 'middle';
                ctx.fillStyle = '#000';
                
                const text = `${Math.min(100, Math.round(progress))}%`;
                const textX = Math.round((width - ctx.measureText(text).width) / 2);
                const textY = height / 2;
                
                ctx.fillText(text, textX, textY);
                ctx.save();
            }
        });
    });
});
