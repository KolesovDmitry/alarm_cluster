from itertools import chain
import uuid



def uniq_name(prefix='nd_'):
    return prefix + uuid.uuid4().hex



class MapcalcPerceptron:
    def __init__(self, ww, bb):
        """
        ww: list of weights,
        bb: list of biases
        """
        assert len(ww) == len(bb)
        # Transpose the weights because of different row order in matrix multiplication and loop over neurons 
        # (see mapcalc's implementation of neuron)
        self._ww = []
        for w in ww:
            transposed = map(list, zip(*w))
            self._ww.append(transposed)
        self._bb = bb


    @property
    def layer_count(self):
        return len(self._ww)

    def _relu(self, node):
        expr = 'if(%s>0, %s)' % (node, node)
        return expr

    def _sigmoid(self, node):
        expr = '1.0 / (1 + exp(-(%s)))' % (node, )
        return expr



    def _layer(self, x, w, b, activation, out_names=[]):
        """Return sum(xi * wi) + b

        x is 1d list of raster names
        w is list of 1d lists of numbers
        b is 1d list of numbers
        activation is activation function
        out_names is list of output neurons

        return list of tuples ([raster_names], [expression to evaluate the rasters])
        """
        assert len(b) == len(w)
        if not out_names:
            out_names = [uniq_name() for _ in range(len(b))]
        y = []
        for wi, bi, node in zip(w, b, out_names):
            assert len(x) == len(wi)
            # node = uniq_name()
            s = []
            for xk, wk in zip(x, wi):
                s.append("(%s)*(%s)" % (xk, wk))
            s.append('(%s)' % (bi, ))

            s = '+'.join(s)
            temp_node = uniq_name()
            temp_expr = '%s = %s' % (temp_node, s)
            node_expr = '%s = %s' % (node, activation(temp_node))
            expr = '%s, %s' % (temp_expr, node_expr)
            y.append((node, expr))

        return y

    def _expressions(self, x, outmaps):
        expr = []
        # import ipdb; ipdb.set_trace()
        for i in range(len(self._ww)):
            w = self._ww[i]
            b = self._bb[i]
            inp = [n[0] for n in expr[-1]] if expr else x
            last_layer = (len(expr) == len(self._ww)-1)
            if last_layer:
                names = outmaps
                # import ipdb; ipdb.set_trace()
                expr.append(self._layer(inp, w, b, self._sigmoid, names))
            else:
                expr.append(self._layer(inp, w, b, self._relu, []))
        
        expr = list(chain(*expr))
        calcs = ', \\\n'.join([e[1] for e in expr])

        return calcs

    def output(self, x, outmaps):
        temp_results = [uniq_name() for _ in outmaps]
        expr = self._expressions(x, temp_results)

        eval_stmt = 'eval(%s)' % (expr)
        stmts = [eval_stmt] + ['%s = %s' % (res_name, tmp_name) for (res_name, tmp_name) in zip(outmaps, temp_results)]

        return '\n'.join(stmts)


if __name__ == '__main__':
    w = [
        [
            [0.9, .0, 0.1], 
            [5.2, 2.0, 2.1],
        ],
        [
            [10.0], 
            [10.1], 
            [10.2]
        ],
        [
            [1, 7],
        ]
    ]
    b = [
        [-0.0, -0.1, -0.3], 
        [-1.0],
        [1, 5]
    ]
    perc = MapcalcPerceptron(w, b)
    out = perc.output(['tmp_999', -100], ['result_tmp', 'result1_tmp'])

    print(out)
