from django.contrib import admin

from .models import Author, Book, Genre, Review, CustomUser


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'publication_date', 'average_rating')
    list_filter = ('genre', 'author', 'publication_date')
    search_fields = ('title', 'author__name', 'genre__name')
    ordering = ('-publication_date',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'author', 'rating', 'text')
    list_filter = ('rating', 'book')    
    search_fields = ('book__title', 'author__username', 'text')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    readonly_fields = ('password',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)