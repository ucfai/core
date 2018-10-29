import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def view_classify(img, ps, version="MNIST"):
    """ Function for viewing an image and it's predicted classes.
    """
    ps = ps.data.numpy().squeeze()
    
    fig, (ax1, ax2) = plt.subplots(figsize=(6, 9), ncols=2)
    ax1.imshow(img.resize_(1, 28, 28).numpy().squeeze(), cmap='gray')
    ax1.axis('off')
    ax2.barh(np.arange(10), ps)
    ax2.set_aspect(0.1)
    ax2.set_yticks(np.arange(10))
    if version == "MNIST":
        ax2.set_yticklabels(np.arange(10))
        
    elif version == "Fashion":
        ax2.set_yticklabels(['T-shirt/top',
                             'Trouser',
                             'Pullover',
                             'Dress',
                             'Coat',
                             'Sandal',
                             'Shirt',
                             'Sneaker',
                             'Bag',
                             'Ankle Boot'], size='small')
    
    ax2.set_title('Class Probability')
    ax2.set_xlim(0, 1.1)
    
    plt.tight_layout()


def plot_loss_acc(loss, accy):
    plt.style.use("seaborn-darkgrid")

    fig, (ax1, ax2) = plt.subplots(figsize=(12, 4), ncols=2)

    ax1.plot(np.arange(10), loss)
    ax1.set_title("Average Loss, per Epoch")

    ax2.plot(np.arange(10), accy)
    ax2.set_title("Average Accuracy, per Epoch")
    
    plt.tight_layout()
