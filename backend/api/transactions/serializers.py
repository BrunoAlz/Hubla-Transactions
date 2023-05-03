from rest_framework import serializers
from .models import Contract, Transaction, TransactionType, Report


class ContractRegisterSerializer(serializers.ModelSerializer):
    """
    A serializer for creating a new Contract object.

    """
    class Meta:
        model = Contract
        fields = ['upload']

    def create(self, validated_data):
        """
        Returns:
            A new Contract object created with the validated data 
            and the authenticated user as the creator.
        """
        user = self.context.get('user')
        instance = Contract(upload=validated_data['upload'], creator=user)
        instance.save()
        return instance


class ContractListSerializer(serializers.ModelSerializer):
    """
     A serializer for retrieving a list of Contract 
     objects created by the authenticated user.
    """
    first_name = serializers.CharField(
        source='creator.first_name', read_only=True)
    last_name = serializers.CharField(
        source='creator.last_name', read_only=True)

    class Meta:
        model = Contract
        fields = ['id', 'first_name', 'last_name',
                  'created_at', 'upload', 'status']


class TransactionsTypeSerializer(serializers.ModelSerializer):
    """
        A serializer for retrieving TransactionType objects.
    """
    class Meta:
        model = TransactionType
        fields = '__all__'


class ContractTransactionsSerializer(serializers.ModelSerializer):
    """
    A serializer for retrieving a list of Transaction objects
    associated with a Contract.

    `description, nature and signal:` are being accessed through the
    relationship in the database so that more information is displayed
    to the user.
    """
    description = serializers.CharField(
        source='type.description', read_only=True)

    nature = serializers.CharField(
        source='type.nature', read_only=True)

    signal = serializers.CharField(
        source='type.signal', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'type', 'contract',
                  'date', 'product', 'price', 'seller', 'description',
                  'nature', 'signal']


class ReportSerializer(serializers.ModelSerializer):
    """
        A serializer for retrieving Report objects.
    """
    class Meta:
        model = Report
        fields = '__all__'


class ContractDetailSerializer(serializers.ModelSerializer):
    """
    A serializer for retrieving a detailed representation of a Contract
    including associated transactions and a report.

    Attributes:
        `transactio_contract` (ContractTransactionsSerializer): A nested
        serializer for retrieving a list of Transactions
        associated with the Contract.

        `report (method)`: A method for retrieving the first Report object
        associated with the Contract.

        `Returns:`
            dict or None: The serialized representation of the first Report
            object, or None if no Report is associated with the Contract.
    """
    transactio_contract = ContractTransactionsSerializer(many=True)
    report = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = ['transactio_contract', 'report']

    def get_report(self, obj):

        report = obj.report.first()
        if report:
            return ReportSerializer(report).data
        else:
            return None
