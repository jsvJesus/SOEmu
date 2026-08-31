# Embedded file name: scripts/common/matrix_providers.py
import BigWorld
import Math

def ShiftProvider(matrix, shift):
    shift_matrix = Math.Matrix(matrix)
    shift_matrix.setTranslate(shift)
    shifted_prov = Math.MatrixProduct()
    shifted_prov.a = matrix
    shifted_prov.b = shift_matrix
    return shifted_prov


def ScaleProvider(source_provider, scale):
    scaled_matrix = Math.Matrix()
    scaled_matrix.setScale(scale)
    scaled_product = Math.MatrixProduct()
    scaled_product.a = scaled_matrix
    scaled_product.b = source_provider
    return scaled_product