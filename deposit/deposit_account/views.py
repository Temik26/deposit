from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import DepositSerializer
from .business_logic import calculation


class DepositCalculationView(APIView):
    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        if not serializer.is_valid():
            error_key = list(serializer.errors.keys())[0]
            error = serializer.errors[error_key][0]
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        deposit = calculation.DepositDetails(**serializer.data)
        calculated_deposit = calculation.calculate_deposit(deposit.date,
                                                           deposit.periods,
                                                           deposit.amount,
                                                           deposit.rate)
        return Response(calculated_deposit, status=status.HTTP_200_OK)

