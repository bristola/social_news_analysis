import matplotlib.pyplot as plt
from io import BytesIO
import base64

t = BytesIO()
plt.plot([1,2,3,4])
plt.savefig(t)
encoded = base64.b64encode(t.getvalue())
encoded_str = str(encoded)
encoded_str = encoded_str[2:len(encoded_str)-1]
print(encoded_str)
