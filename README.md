# final_project_creditscoring

# Objetivo general
Desarrollar un modelo de Credit Scoring basado en Machine Learning que permita predecir el riesgo de impago de los clientes de retail.
#Objetivos específicos
- Reducir pérdidas financieras por créditos impagos
- Mejorar la toma de decisiones en la aprobación de crédito
- Clasificar clientes según su nivel de riesgo
- Automatizar y estandarizar el proceso de evaluación crediticia

Los datos utilizados en este proyecto provienen del Lending Club Loan Data, un conjunto de datos públicos de préstamos emitidos por la plataforma de financiamiento peer-to-peer Lending Club en Estados Unidos. Este dataset incluye información de los solicitantes, características de los préstamos y el estado final de los mismos, lo que permite analizar y predecir el riesgo de impago.

## Variables de entrada

### A) Características del préstamo
•	loan_amnt → monto solicitado
•	term → duración del préstamo (36/60 meses)
•	int_rate → tasa de interés
•	installment → valor mensual a pagar
•	purpose → motivo del préstamo (educación, coche, vivienda…)
•	grade / sub_grade → calificación interna del cliente
### B) Características financieras del solicitante
•	annual_inc → ingreso anual
•	dti → ratio deuda-ingreso
•	revol_bal → deuda rotativa actual
•	revol_util → porcentaje de utilización de la línea de crédito
•	total_acc → número total de cuentas de crédito
•	open_acc → cuentas abiertas
•	pub_rec → registros públicos negativos (ej. quiebras)
•	delinq_2yrs → número de atrasos en los últimos 2 años
### C) Historial crediticio
•	earliest_cr_line → fecha de apertura de la primera línea de crédito
•	inq_last_6mths → consultas de crédito recientes
•	mths

## Variable de salida (target)
Variable objetivo (y): loan_status reclasificada como binaria

El modelo aprende a partir de datos históricos para predecir la probabilidad de impago de un nuevo solicitante, además también se tiene se tendrá en cuenta variables macroeconómicas y cómo estas podrían afectar al incumplimiento del pago.

## Preguntas clave que el análisis de datos debe responder
¿Qué características de un cliente están más asociadas al impago?
¿Cuál es la probabilidad de que un cliente no pague su crédito?
¿Qué clientes representan mayor riesgo crediticio?
¿Dónde establecer el umbral de aprobación del crédito?
¿Cómo impacta el monto del crédito en la probabilidad de impago?


