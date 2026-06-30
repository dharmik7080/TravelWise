from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum
from trips.models import Trip

class DashboardIndexView(LoginRequiredMixin, TemplateView):
    """
    Main user dashboard view displaying custom travel metrics,
    upcoming itineraries, past trips, and placeholders for travel tips/charts.
    """
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        local_time = timezone.localtime(timezone.now())
        current_date = local_time.date()

        # Define welcome greeting dynamically based on local hour
        hour = local_time.hour
        if hour < 12:
            greeting = "Good Morning"
        elif hour < 18:
            greeting = "Good Afternoon"
        else:
            greeting = "Good Evening"
        
        context['greeting'] = greeting
        context['current_date'] = current_date

        # Retrieve statistics for current traveler using optimized conditional aggregation
        from django.db.models import Count, Avg, Q
        user_trips = Trip.objects.filter(user=user).select_related('destination')
        stats = user_trips.aggregate(
            total=Count('id'),
            upcoming=Count('id', filter=Q(start_date__gte=current_date)),
            completed=Count('id', filter=Q(end_date__lt=current_date)),
            avg_budget=Avg('budget')
        )
        context['total_trips'] = stats['total']
        context['upcoming_count'] = stats['upcoming']
        context['completed_count'] = stats['completed']
        context['average_budget'] = stats['avg_budget'] or 0

        # Group trips into upcoming vs. past categories
        context['upcoming_trips'] = user_trips.filter(start_date__gte=current_date).order_by('start_date')[:5]
        context['recent_trips'] = user_trips.order_by('-created_at')[:5]

        # Retrieve travel insights dynamically using Django ORM
        from django.db.models import ExpressionWrapper, F, Avg
        from django.db.models.fields import DurationField

        most_visited = user_trips.values('destination__destination_name').annotate(count=Count('id')).order_by('-count').first()
        context['most_visited_dest'] = most_visited['destination__destination_name'] if most_visited else None

        highest_budget_trip = user_trips.order_by('-budget').first()
        context['highest_budget_trip'] = highest_budget_trip

        duration_expr = ExpressionWrapper(F('end_date') - F('start_date'), output_field=DurationField())
        avg_duration_delta = user_trips.annotate(duration=duration_expr).aggregate(avg=Avg('duration'))['avg']
        context['avg_duration_days'] = avg_duration_delta.days + 1 if avg_duration_delta else 0

        most_common = user_trips.values('travel_type').annotate(count=Count('id')).order_by('-count').first()
        context['most_common_type'] = most_common['travel_type'] if most_common else None

        # Generate Plotly charts dynamically
        context['has_charts'] = False
        if stats['total'] > 0:
            import plotly.graph_objects as go
            from plotly.offline import plot
            from django.db.models.functions import TruncMonth

            # 1. Trips by Month
            monthly_trips = user_trips.annotate(month=TruncMonth('start_date')).values('month').annotate(count=Count('id')).order_by('month')
            months = [m['month'].strftime('%b %Y') for m in monthly_trips]
            counts = [m['count'] for m in monthly_trips]
            fig1 = go.Figure(data=go.Bar(
                x=months, 
                y=counts, 
                marker_color='#0d6efd',
                text=counts,
                textposition='auto'
            ))
            fig1.update_layout(
                xaxis_title='Month',
                yaxis_title='Trips Count',
                margin=dict(l=10, r=10, t=10, b=10),
                height=260,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins, sans-serif", size=11)
            )
            context['chart_trips_by_month'] = plot(fig1, output_type='div', include_plotlyjs=False)

            # 2. Budget Distribution
            dest_names = [t.destination.destination_name for t in user_trips]
            budgets = [float(t.budget) for t in user_trips]
            fig2 = go.Figure(data=go.Bar(
                x=dest_names, 
                y=budgets, 
                marker_color='#198754',
                text=[f"${b:,.0f}" for b in budgets],
                textposition='auto'
            ))
            fig2.update_layout(
                xaxis_title='Destination',
                yaxis_title='Budget ($)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=260,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins, sans-serif", size=11)
            )
            context['chart_budget_distribution'] = plot(fig2, output_type='div', include_plotlyjs=False)

            # 3. Travel Type Distribution
            travel_types = user_trips.values('travel_type').annotate(count=Count('id'))
            labels = [t['travel_type'] for t in travel_types]
            values = [t['count'] for t in travel_types]
            fig3 = go.Figure(data=go.Pie(
                labels=labels, 
                values=values, 
                hole=.3,
                marker=dict(colors=['#0d6efd', '#198754', '#ffc107', '#0dcaf0'])
            ))
            fig3.update_layout(
                margin=dict(l=10, r=10, t=10, b=10),
                height=260,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Poppins, sans-serif", size=11)
            )
            context['chart_travel_type_distribution'] = plot(fig3, output_type='div', include_plotlyjs=False)
            context['has_charts'] = True

        return context


class PredictionsView(LoginRequiredMixin, TemplateView):
    """
    Placeholder view for coming flight delay AI predictions.
    """
    template_name = 'dashboard/predictions.html'
