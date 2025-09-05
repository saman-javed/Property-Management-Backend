from rest_framework import serializers

from offices.models import Office
from towns_projects.models import Project, Town
from .models import ExpenseCategory, Expense
from rest_framework import serializers
from .models import Expense, ExpenseCategory
from towns_projects.serializers import TownSerializer, ProjectSerializer
from offices.serializers import OfficeSerializer

class ExpenseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = "__all__"



# class ExpenseSerializer(serializers.ModelSerializer):
#     town = TownSerializer(read_only=True)
#     project = ProjectSerializer(read_only=True)
#     office = OfficeSerializer(read_only=True)
#     category = ExpenseCategorySerializer(read_only=True)

#     class Meta:
#         model = Expense
#         fields = "__all__"


# class ExpenseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Expense
#         fields = '__all__'





class ExpenseSerializer(serializers.ModelSerializer):
    # write-only ID fields
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), source="project", write_only=True
    )
    town_id = serializers.PrimaryKeyRelatedField(
        queryset=Town.objects.all(), source="town", write_only=True
    )
    office_id = serializers.PrimaryKeyRelatedField(
        queryset=Office.objects.all(), source="office", write_only=True
    )
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=ExpenseCategory.objects.all(), source="category", write_only=True
    )

    # read-only nested fields
    project = ProjectSerializer(read_only=True)
    town = TownSerializer(read_only=True)
    office = OfficeSerializer(read_only=True)
    category = ExpenseCategorySerializer(read_only=True)

    class Meta:
        model = Expense
        fields = "__all__"
