from tensorflow.keras import models, Model

#load the model
model = models.load_model('it_threat_model')

# generate embedding using dense layer
layer_name = 'dense'
intermediate_layer_model = Model(
    inputs=model.input,
    outputs=model.get_layer(layer_name).output
)
