import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# Data generators
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    validation_split=0.2
)

train_data = train_datagen.flow_from_directory(
    "dataset",
    target_size=(224, 224),
    batch_size=8,
    class_mode="categorical",
    subset="training",
    shuffle=True
)

val_data = train_datagen.flow_from_directory(
    "dataset",
    target_size=(224, 224),
    batch_size=8,
    class_mode="categorical",
    subset="validation",
    shuffle=False
)

print("Training Images :", train_data.samples)
print("Validation Images :", val_data.samples)

# Save class names
with open("class_indices.json", "w") as f:
    json.dump(train_data.class_indices, f)

# CNN Model
model = Sequential([
    Input(shape=(224, 224, 3)),

    Conv2D(32, (3, 3), activation="relu"),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation="relu"),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation="relu"),
    MaxPooling2D(2, 2),

    Flatten(),

    Dense(128, activation="relu"),
    Dropout(0.5),

    Dense(train_data.num_classes, activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

callbacks = [
    EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True
    ),

    ModelCheckpoint(
        "crop_disease_model.h5",
        monitor="val_accuracy",
        save_best_only=True
    )
]

model.fit(
    train_data,
    validation_data=val_data,
    epochs=15,
    verbose=1,
    callbacks=callbacks
)

model.save("crop_disease_model.h5")

print("\n===================================")
print("✅ Training Completed Successfully")
print("✅ Model Saved : crop_disease_model.h5")
print("✅ Class Index Saved : class_indices.json")
print("===================================")