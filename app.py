from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Sample data structure to store contributions and groups
contributions = []
groups = []


# Create a contribution group over REST using JSON
@app.route('/create_group', methods=['POST'])
def create_group():
    # Extract group_name from the form submission and create a group
    group_name = request.form.get('group_name')
    groups.append({'group_id': len(groups) + 1, 'group_name': group_name})
    return jsonify({'message': 'Contribution group created successfully'})


@app.route('/record_contribution', methods=['POST'])
def record_contribution():
    # Extract email, amount, and group_id from the form submission and record the contribution
    email = request.form.get('email')
    amount = request.form.get('amount')
    group_id = request.form.get('group_id')

    # Check if the group exists
    group = next((g for g in groups if g['group_id'] == int(group_id)), None)
    if group is None:
        return jsonify({'error': 'Contribution group not found'})

    contributions.append({'email': email, 'amount': amount, 'group_id': int(group_id)})
    return jsonify({'message': 'Contribution recorded successfully'})


# Get statistics for a contribution group
@app.route('/contribution_stats/<int:group_id>', methods=['GET'])
def contribution_stats(group_id):
    group = next((g for g in groups if g['group_id'] == group_id), None)
    if group is None:
        return jsonify({'error': 'Contribution group not found'})

    group_contributions = [c for c in contributions if c['group_id'] == group_id]
    total_contributors = len(set(c['email'] for c in group_contributions))
    total_raised = sum(int(c['amount']) for c in group_contributions)

    return jsonify({
        'group_name': group['group_name'],
        'total_contributors': total_contributors,
        'total_raised': total_raised
    })


# Get the contribution list in JSON format
@app.route('/contribution_list', methods=['GET'])
def contribution_list():
    return jsonify(contributions)


@app.route('/create_group_form', methods=['GET'])
def create_group_form():
    return render_template('create_group.html')


@app.route('/record_contribution_form', methods=['GET'])
def record_contribution_form():
    return render_template('record_contribution.html')


@app.route('/contribution_stats_page/<int:group_id>', methods=['GET'])
def contribution_stats_page(group_id):
    return render_template('stats.html', group_id=group_id)


if __name__ == '__main__':
    app.run(debug=True)
