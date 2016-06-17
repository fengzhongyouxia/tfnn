import tfnn
import matplotlib.pyplot as plt
plt.style.use('ggplot')


class Evaluator(object):
    def __init__(self, network, ):
        self.network = network
        if isinstance(self.network, tfnn.ClassificationNetwork):
            with tfnn.name_scope('accuracy'):
                correct_prediction = tfnn.equal(tfnn.argmax(network.predictions, 1),
                                              tfnn.argmax(network.target_placeholder, 1), name='correct_prediction')
                self.accuracy = tfnn.reduce_mean(tfnn.cast(correct_prediction, tfnn.float32), name='accuracy')
                tfnn.scalar_summary('accuracy', self.accuracy)
        elif isinstance(self.network, tfnn.RegressionNetwork):
            self.first_time = True

    def compute_accuracy(self, xs, ys):
        if not isinstance(self.network, tfnn.ClassificationNetwork):
            raise NotImplementedError('Can only compute accuracy for Classification neural network.')

        if self.network.reg == 'dropout':
            feed_dict = {self.network.data_placeholder: xs,
                         self.network.target_placeholder: ys,
                         self.network.keep_prob_placeholder: 1.}
        elif self.network.reg == 'l2':
            feed_dict = {self.network.data_placeholder: xs,
                         self.network.target_placeholder: ys,
                         self.network.l2_placeholder: 0.}
        else:
            feed_dict = {self.network.data_placeholder: xs,
                         self.network.target_placeholder: ys}

        return self.accuracy.eval(feed_dict, self.network.sess)

    def compute_cost(self, xs, ys):
        if self.network.reg == 'dropout':
            feed_dict = {self.network.data_placeholder: xs,
                         self.network.target_placeholder: ys,
                         self.network.keep_prob_placeholder: 1.}
        elif self.network.reg == 'l2':
            feed_dict = {self.network.data_placeholder: xs,
                         self.network.target_placeholder: ys,
                         self.network.l2_placeholder: 0.}
        else:
            feed_dict = {self.network.data_placeholder: xs,
                         self.network.target_placeholder: ys}
        return self.network.loss.eval(feed_dict, self.network.sess)

    def plot_single_output_comparison(self, v_xs, v_ys, continue_plot=False):
        """
        Suitable for analysing the datasets with only one output unit.
        :param v_xs: validated xs
        :param v_ys: validated ys (single attribute)
        :param continue_plot: True or False
        :return: Plotting
        """
        if not isinstance(self.network, tfnn.RegressionNetwork):
            raise NotImplementedError('Can only compute accuracy for Regression neural network.')
        if self.network.reg == 'dropout':
            feed_dict = {self.network.data_placeholder: v_xs,
                         self.network.target_placeholder: v_ys,
                         self.network.keep_prob_placeholder: 1.}
        elif self.network.reg == 'l2':
            feed_dict = {self.network.data_placeholder: v_xs,
                         self.network.target_placeholder: v_ys,
                         self.network.l2_placeholder: 0.}
        else:
            feed_dict = {self.network.data_placeholder: v_xs,
                         self.network.target_placeholder: v_ys}
        predictions = self.network.predictions.eval(feed_dict, self.network.sess)
        fig, ax = plt.subplots()
        ax.scatter(v_ys, predictions, label='predicted')
        ax.plot([v_ys.min(), v_ys.max()], [v_ys.min(), v_ys.max()], 'r--', lw=4, label='real')
        ax.grid(True)
        ax.legend()
        ax.set_xlabel('Real data')
        ax.set_ylabel('Predicted')

        if self.first_time:
            self.first_time = False
            if continue_plot:
                plt.ion()
            plt.pause(0.5)
            plt.show()
        else:
            plt.pause(0.001)
            plt.close(fig)
            plt.draw()

    def plot_line_matching(self, v_xs, v_ys, continue_plot=False):
        """
        Suitable for analysing the dataset with only one attribute and single output.
        :param v_xs: Only has one attribute
        :param v_ys: Only has one attribute
        :param continue_plot: True or False
        :return: plotting
        """
        if not isinstance(self.network, tfnn.RegressionNetwork):
            raise NotImplementedError('Can only compute accuracy for Regression neural network.')
        if self.network.reg == 'dropout':
            feed_dict = {self.network.data_placeholder: v_xs,
                         self.network.target_placeholder: v_ys,
                         self.network.keep_prob_placeholder: 1.}
        elif self.network.reg == 'l2':
            feed_dict = {self.network.data_placeholder: v_xs,
                         self.network.target_placeholder: v_ys,
                         self.network.l2_placeholder: 0.}
        else:
            feed_dict = {self.network.data_placeholder: v_xs,
                         self.network.target_placeholder: v_ys}
        predictions = self.network.predictions.eval(feed_dict, self.network.sess)
        fig, ax = plt.subplots()
        ax.scatter(v_xs, v_ys, c='red', s=20)
        ax.scatter(v_xs, predictions, c='blue', s=20)
        ax.set_xlabel('Input')
        ax.set_ylabel('Output')
        if self.first_time:
            self.first_time = False
            if continue_plot:
                plt.ion()
            plt.pause(0.5)
            plt.show()
        else:
            plt.pause(0.1)
            plt.close(fig)
            plt.draw()

