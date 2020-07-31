import graphene
from graphene_django.types import DjangoObjectType
from ingredients.models import Category, Ingredient
from graphene import ObjectType


""" Define types """


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class Query(object):
    """ Queries for Categories """
    category = graphene.Field(
        CategoryType, id=graphene.Int(), name=graphene.String())
    all_categories = graphene.List(CategoryType)

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(id=id)
        if name is not None:
            return Category.objects.get(name=name)
        return None

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    """ Queries for Ingredients """
    ingredient = graphene.Field(
        IngredientType, id=graphene.Int(), name=graphene.String())
    all_ingredients = graphene.List(IngredientType)

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Ingredient.objects.get(id=id)
        if name is not None:
            return Ingredient.objects.get(name=name)
        return None

    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.select_related('category').all()


"""  """


class CategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(root, info, name):
        category = Category.objects.create(name=name)
        return CategoryMutation(category=category)


class Mutation(ObjectType):
    create_category = CategoryMutation.Field()
