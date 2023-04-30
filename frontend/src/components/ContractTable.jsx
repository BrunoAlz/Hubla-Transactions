import ContractStatus from "./ContractStatus";

const ContractTable = ({ props }) => {
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
            props.map((contract) => (
              <tr key={contract.id}>
                <th scope="row">{contract.id}</th>
                <td>{contract.created_at}</td>
                <td>{contract.upload}</td>
                <td className="fw-bold">
                  {contract.first_name} {contract.last_name}
                </td>
                <td>
                  <ContractStatus props={contract.status} />
                </td>
              </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default ContractTable;
