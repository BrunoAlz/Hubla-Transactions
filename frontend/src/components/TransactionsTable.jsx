const TransactionsTable = ({props}) => {

  return (
    <div>
      <table className="table table-striped table-sm table-hover text-center mt-5">
        <thead>
          <tr className="fw-bold fs-5">
            <th>N°</th>
            <th>Date</th>
            <th>File</th>
            <th>Owner</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {props &&
            props.map((transaction) => (
              <tr key={transaction.id}>
                <th scope="row">{transaction.id}</th>
                <td>{transaction.date}</td>
                <td>{transaction.product}</td>
                <td>{transaction.price}</td>
                <td>{transaction.seller}</td>
                <td>{transaction.type}</td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default TransactionsTable;
