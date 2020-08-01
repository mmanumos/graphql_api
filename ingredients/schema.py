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


""" Mutations """


class IngredientData(graphene.InputObjectType):
    name = graphene.String(required=True)
    notes = graphene.String()


class CreateCategory(graphene.Mutation):
    """ Creat category """
    class Arguments:
        name = graphene.String(required=True)
        ingredients_list = graphene.List(IngredientData)

    category = graphene.Field(CategoryType)

    def mutate(self, info, name, ingredients_list=None):
        obj = Category.objects.create(name=name)
        if ingredients_list is not None:
            for data in ingredients_list:
                obj_sub = Ingredient.objects.create(
                    name=data.name, notes=data.notes, category=obj)
        return CreateCategory(category=obj)


class UpdateCategory(graphene.Mutation):
    """ Update category """
    class Arguments:
        id = graphene.Int()
        name = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(self, info, id, name):
        obj = Category.objects.create(name=name)
        try:
            obj = Category.objects.get(id=id)
            obj.name = name
            obj.save()
            return UpdateCategory(category=obj)
        except Exception:
            return None


class Mutation(ObjectType):
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
