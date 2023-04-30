import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { toast } from "react-toastify";

const Table = ({ props }) => {
  return (
    <table className="table table-striped table-hover mt-5">
      <thead>
        <tr>
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
              <td>{contract.creator}</td>
              <td>{contract.status}</td>
            </tr>
          ))}
      </tbody>
    </table>
  );
};

export default Table;
