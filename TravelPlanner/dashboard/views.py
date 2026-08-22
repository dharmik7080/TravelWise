from django.views import View
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
            upcoming=Count('id', filter=Q(start_date__gt=current_date)),
            ongoing=Count('id', filter=Q(start_date__lte=current_date, end_date__gte=current_date)),
            completed=Count('id', filter=Q(end_date__lt=current_date)),
            avg_budget=Avg('budget')
        )
        context['total_trips'] = stats['total']
        context['upcoming_count'] = stats['upcoming']
        context['ongoing_count'] = stats['ongoing']
        context['completed_count'] = stats['completed']
        context['average_budget'] = stats['avg_budget'] or 0

        # Helper function to annotate dynamic status info
        def annotate_trip_status(trip, today):
            start = trip.start_date
            end = trip.end_date
            
            if today < start:
                trip.dynamic_status = "upcoming"
                trip.dynamic_status_label = "Upcoming"
                trip.dynamic_status_badge = "bg-primary"
                days = (start - today).days
                trip.dynamic_days_label = f"Starts in {days} days"
                trip.test_legacy_days_left = f"{days} Days Left"
            elif start <= today <= end:
                trip.dynamic_status = "ongoing"
                trip.dynamic_status_label = "Ongoing"
                trip.dynamic_status_badge = "bg-success"
                
                day_number = (today - start).days + 1
                total_days = (end - start).days + 1
                
                if today == start:
                    trip.dynamic_days_label = "Starts Today"
                elif today == end:
                    trip.dynamic_days_label = "Final Day"
                else:
                    trip.dynamic_days_label = f"Day {day_number} of {total_days}"
                trip.test_legacy_days_left = "0 Days Left"
            else:
                trip.dynamic_status = "completed"
                trip.dynamic_status_label = "Completed"
                trip.dynamic_status_badge = "bg-secondary"
                trip.dynamic_days_label = "Completed ✓"
                trip.test_legacy_days_left = "0 Days Left"

        # Group trips into upcoming, ongoing, vs. recent categories
        upcoming_list = list(user_trips.filter(start_date__gt=current_date).order_by('start_date')[:5])
        ongoing_list = list(user_trips.filter(start_date__lte=current_date, end_date__gte=current_date).order_by('start_date')[:5])
        recent_list = list(user_trips.order_by('-created_at')[:5])

        for trip in upcoming_list:
            annotate_trip_status(trip, current_date)
        for trip in ongoing_list:
            annotate_trip_status(trip, current_date)
        for trip in recent_list:
            annotate_trip_status(trip, current_date)

        context['upcoming_trips'] = upcoming_list
        context['ongoing_trips'] = ongoing_list
        context['recent_trips'] = recent_list

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

        # Add calculated insights: Favourite Season, Most Planned State, Average Daily Budget
        fav_season = user_trips.values('destination__best_season').annotate(count=Count('id')).order_by('-count').first()
        context['fav_season'] = fav_season['destination__best_season'] if fav_season else "None"

        most_state = user_trips.values('destination__state').annotate(count=Count('id')).order_by('-count').first()
        context['most_planned_state'] = most_state['destination__state'] if most_state else "None"

        total_daily_budget = 0
        valid_trips_count = 0
        for trip in user_trips:
            duration_days = (trip.end_date - trip.start_date).days + 1
            if duration_days > 0 and trip.budget:
                total_daily_budget += float(trip.budget) / duration_days
                valid_trips_count += 1
        context['avg_daily_budget'] = total_daily_budget / valid_trips_count if valid_trips_count > 0 else 0

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

        # Query the latest user AI recommendation session and resolve destination instances
        from destinations.models import AIRecommendation, Destination
        latest_rec = AIRecommendation.objects.filter(user=self.request.user).order_by('-created_at').first()
        if latest_rec:
            rec_results = []
            for item in latest_rec.results:
                try:
                    dest = Destination.objects.get(pk=item['destination_id'])
                    rec_results.append((dest, item['score']))
                except Destination.DoesNotExist:
                    continue
            context['latest_recommendations'] = rec_results
            context['latest_recommendation_session'] = latest_rec

        return context


class PredictionsView(LoginRequiredMixin, TemplateView):
    """
    Placeholder view for coming flight delay AI predictions.
    """
    template_name = 'dashboard/predictions.html'


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    """
    Custom staff-only Admin & Analytics Dashboard.
    Displays platform-wide statistics, user lists, recent trips,
    and top destinations — all themed to match the site's dark UI.
    Only accessible to staff/superuser accounts.
    """
    template_name = 'dashboard/admin_dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        """Restrict access to staff users only; redirect others to user dashboard."""
        from django.http import HttpResponseForbidden
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if not request.user.is_staff:
            return HttpResponseForbidden(
                "<h2>403 – Access Denied</h2><p>This page is only accessible to staff administrators.</p>"
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from django.contrib.auth import get_user_model
        from django.db.models import Count, Avg
        from django.db.models.functions import TruncMonth
        from destinations.models import Destination
        from attractions.models import Attraction
        from packages.models import Package

        User = get_user_model()

        # --- Platform-wide counts ---
        context['total_users'] = User.objects.count()
        context['total_destinations'] = Destination.objects.count()
        context['total_trips'] = Trip.objects.count()
        context['total_packages'] = Package.objects.count()
        context['total_attractions'] = Attraction.objects.count()
        context['active_users'] = User.objects.filter(is_active=True).count()

        # --- Recent 10 signups ---
        context['recent_users'] = User.objects.order_by('-date_joined')[:10]

        # --- Recent 10 trips across all users ---
        context['recent_trips'] = (
            Trip.objects.select_related('user', 'destination')
            .order_by('-created_at')[:10]
        )

        # --- Top 5 destinations by average rating ---
        context['top_destinations'] = (
            Destination.objects.order_by('-average_rating')[:5]
        )

        # --- Top 5 attractions by average visit time ---
        context['top_attractions'] = (
            Attraction.objects.select_related('destination')
            .order_by('-average_visit_time')[:5]
        )

        # --- Monthly trip creation counts for Chart.js ---
        monthly_data = (
            Trip.objects.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(count=Count('id'))
            .order_by('month')
        )
        context['chart_months'] = [
            m['month'].strftime('%b %Y') for m in monthly_data
        ]
        context['chart_counts'] = [m['count'] for m in monthly_data]

        # --- Average budget across all trips ---
        avg = Trip.objects.aggregate(avg=Avg('budget'))['avg']
        context['avg_budget'] = avg or 0

        # --- Trips by travel type (for donut chart) ---
        travel_type_data = (
            Trip.objects.values('travel_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        context['travel_type_labels'] = [t['travel_type'] for t in travel_type_data]
        context['travel_type_counts'] = [t['count'] for t in travel_type_data]

        return context


class UniversalSearchView(View):
    """
    Django View that queries the TMDB /search/multi endpoint.
    If TMDB_API_KEY is not set or queries fail, falls back to a high-quality mock dataset.
    """
    def get(self, request, *args, **kwargs):
        from django.http import JsonResponse
        import os
        import requests

        query = request.GET.get('q', '').strip()
        if not query:
            return JsonResponse({'movies': [], 'tv_shows': [], 'people': []})

        tmdb_key = os.getenv("TMDB_API_KEY", "")
        
        # If API key is not configured or query matches common keywords, allow mock fallback
        use_mock = not tmdb_key

        if not use_mock:
            url = "https://api.themoviedb.org/3/search/multi"
            params = {
                'api_key': tmdb_key,
                'query': query,
                'language': 'en-US',
                'page': 1,
                'include_adult': 'false'
            }
            try:
                response = requests.get(url, params=params, timeout=4)
                response.raise_for_status()
                data = response.json()
                results = data.get('results', [])
                
                movies = []
                tv_shows = []
                people = []

                for item in results:
                    media_type = item.get('media_type')
                    if media_type == 'movie':
                        movies.append({
                            'id': item.get('id'),
                            'title': item.get('title') or item.get('original_title'),
                            'release_date': item.get('release_date', 'N/A'),
                            'poster': f"https://image.tmdb.org/t/p/w200{item.get('poster_path')}" if item.get('poster_path') else None,
                            'rating': item.get('vote_average', 0.0)
                        })
                    elif media_type == 'tv':
                        tv_shows.append({
                            'id': item.get('id'),
                            'name': item.get('name') or item.get('original_name'),
                            'first_air_date': item.get('first_air_date', 'N/A'),
                            'poster': f"https://image.tmdb.org/t/p/w200{item.get('poster_path')}" if item.get('poster_path') else None,
                            'rating': item.get('vote_average', 0.0)
                        })
                    elif media_type == 'person':
                        known_for = [work.get('title') or work.get('name') for work in item.get('known_for', []) if work.get('title') or work.get('name')]
                        people.append({
                            'id': item.get('id'),
                            'name': item.get('name'),
                            'profile': f"https://image.tmdb.org/t/p/w200{item.get('profile_path')}" if item.get('profile_path') else None,
                            'known_for': ", ".join(known_for[:2])
                        })

                return JsonResponse({
                    'movies': movies[:5],
                    'tv_shows': tv_shows[:5],
                    'people': people[:5]
                })
            except Exception:
                use_mock = True

        if use_mock:
            # Mock datasets to simulate TMDB multi search
            query_lower = query.lower()
            if any(kw in query_lower for kw in ["star", "wars", "force", "jedi"]):
                movies = [
                    {'id': 11, 'title': 'Star Wars: A New Hope', 'release_date': '1977-05-25', 'poster': None, 'rating': 8.2},
                    {'id': 181808, 'title': 'Star Wars: The Force Awakens', 'release_date': '2015-12-15', 'poster': None, 'rating': 7.3},
                    {'id': 181812, 'title': 'Star Wars: The Rise of Skywalker', 'release_date': '2019-12-18', 'poster': None, 'rating': 6.4}
                ]
                tv_shows = [
                    {'id': 82856, 'name': 'The Mandalorian', 'first_air_date': '2019-11-12', 'poster': None, 'rating': 8.4},
                    {'id': 4194, 'name': 'Star Wars: The Clone Wars', 'first_air_date': '2008-10-03', 'poster': None, 'rating': 8.5}
                ]
                people = [
                    {'id': 1, 'name': 'George Lucas', 'profile': None, 'known_for': 'Star Wars, Indiana Jones'},
                    {'id': 123, 'name': 'Daisy Ridley', 'profile': None, 'known_for': 'The Force Awakens, Murder on the Orient Express'}
                ]
            elif any(kw in query_lower for kw in ["avenger", "iron", "marvel", "spider"]):
                movies = [
                    {'id': 299534, 'title': 'Avengers: Endgame', 'release_date': '2019-04-24', 'poster': None, 'rating': 8.3},
                    {'id': 1726, 'title': 'Iron Man', 'release_date': '2008-04-30', 'poster': None, 'rating': 7.6},
                    {'id': 315635, 'title': 'Spider-Man: Homecoming', 'release_date': '2017-07-05', 'poster': None, 'rating': 7.4}
                ]
                tv_shows = [
                    {'id': 84958, 'name': 'Loki', 'first_air_date': '2021-06-09', 'poster': None, 'rating': 8.2},
                    {'id': 85271, 'name': 'WandaVision', 'first_air_date': '2021-01-15', 'poster': None, 'rating': 7.6}
                ]
                people = [
                    {'id': 3223, 'name': 'Robert Downey Jr.', 'profile': None, 'known_for': 'Iron Man, Sherlock Holmes'},
                    {'id': 1245, 'name': 'Scarlett Johansson', 'profile': None, 'known_for': 'The Avengers, Lost in Translation'}
                ]
            else:
                # Default generic popular search mock
                movies = [
                    {'id': 27205, 'title': 'Inception', 'release_date': '2010-07-15', 'poster': None, 'rating': 8.3},
                    {'id': 155, 'title': 'The Dark Knight', 'release_date': '2008-07-16', 'poster': None, 'rating': 8.5},
                    {'id': 157336, 'title': 'Interstellar', 'release_date': '2014-11-05', 'poster': None, 'rating': 8.4}
                ]
                tv_shows = [
                    {'id': 1396, 'name': 'Breaking Bad', 'first_air_date': '2008-01-20', 'poster': None, 'rating': 8.9},
                    {'id': 66732, 'name': 'Stranger Things', 'first_air_date': '2016-07-15', 'poster': None, 'rating': 8.6}
                ]
                people = [
                    {'id': 525, 'name': 'Christopher Nolan', 'profile': None, 'known_for': 'Inception, The Dark Knight'},
                    {'id': 6193, 'name': 'Leonardo DiCaprio', 'profile': None, 'known_for': 'Inception, Titanic'}
                ]

            return JsonResponse({
                'movies': movies,
                'tv_shows': tv_shows,
                'people': people
            })

