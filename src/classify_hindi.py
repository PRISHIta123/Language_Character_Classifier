def CLASSIFY():
    #!/usr/bin/env python

    import argparse
    import io
    import os
    import sys
    from PIL import Image
    from resizeimage import resizeimage

    import tensorflow as tf


    SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

    # Default paths.
    DEFAULT_LABEL_FILE = os.path.join(
        SCRIPT_PATH, '../Hindi/labels/90-common-hindi.txt'
    )
    DEFAULT_GRAPH_FILE = os.path.join(
        SCRIPT_PATH, '../Hindi/saved-model/optimized_hindi_tensorflow.pb'
    )
    def read_image(file):
        """Read an image file and convert it into a 1-D floating point array."""
        
        file_content = tf.read_file(file)
        image = tf.image.decode_jpeg(file_content, channels=1)
        image = tf.image.convert_image_dtype(image, dtype=tf.float32)
        image = tf.reshape(image, [64*64])
        return image

    label_file='./Hindi/labels/90-common-hindi.txt'
    image='./New3.jpeg'
    graph_file='./Hindi/saved-model/optimized_hindi_tensorflow.pb'
    

    labels = io.open(label_file,
                     'r', encoding='utf-8').read().splitlines()
    # Load graph and parse file.
    with tf.gfile.GFile(graph_file, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    with tf.Graph().as_default() as graph:
        tf.import_graph_def(
            graph_def,
            input_map=None,
            return_elements=None,
            name='hindi-model',
            producer_op_list=None
        )
    # Get relevant nodes.
    x = graph.get_tensor_by_name('hindi-model/input:0')
    y = graph.get_tensor_by_name('hindi-model/output:0')
    keep_prob = graph.get_tensor_by_name('hindi-model/keep_prob:0')
    im = read_image(image)
    sess = tf.InteractiveSession()
    image_array = sess.run(im)
    with tf.Session(graph=graph) as graph_sess:
        predictions = graph_sess.run(y, feed_dict={x: image_array,
                                                   keep_prob: 1.0})
        prediction = predictions[0]
    l=[]
    sorted_indices = prediction.argsort()[::-1][:5]
    for index in sorted_indices:
        label = labels[index]
        l.append(label)
    return l

