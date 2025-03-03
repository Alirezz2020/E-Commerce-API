from django.views.generic import ListView
from shop.models import Product, Category
from django.db.models import Q


class ProductListView(ListView):
    model = Product
    template_name = 'home/home.html'
    context_object_name = 'products'
    paginate_by = 10  # Display 10 products per page

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by search term
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Filter by category if provided
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        # Ordering (default to newest)
        ordering = self.request.GET.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        # Preserve current search/filter values in context for template use.
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['ordering'] = self.request.GET.get('ordering', '-created_at')
        return context
