from rest_framework import serializers

from parallel_lives.models import ParallelLife


class ParallelLifeSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    domains = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = ParallelLife
        fields = [
            "id",
            "owner",
            "title",
            "slug",
            "divergence_date",
            "starting_choice",
            "summary",
            "visibility",
            "status",
            "realism_score",
            "domains",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "slug", "created_at", "updated_at"]
